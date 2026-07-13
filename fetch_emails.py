#!/usr/bin/env python3
import json
import os
import re
import email
import email.utils
import email.header
from datetime import datetime

def decode_header_text(text):
    if not text:
        return ""
    try:
        decoded = email.header.decode_header(text)
        parts = []
        for word, encoding in decoded:
            if isinstance(word, bytes):
                parts.append(word.decode(encoding or "utf-8", errors="ignore"))
            else:
                parts.append(str(word))
        return "".join(parts)
    except Exception:
        return str(text)

def parse_date_to_timestamp(date_str):
    if not date_str:
        return 0
    try:
        # Best approach: Use python's official email date extractor
        dt = email.utils.parsedate_to_datetime(date_str)
        return dt.timestamp()
    except Exception:
        # If it fails, extract any numbers we can find to estimate a order
        try:
            # Fallback regex to find day, month name, year
            match = re.search(r'(\d{1,2})\s+([A-Za-z]{3})\s+(\d{4})\s+(\d{2}):(\d{2})', date_str)
            if match:
                day, mon, year, hr, mn = match.groups()
                dt = datetime.strptime(f"{day} {mon} {year} {hr}:{mn}", "%d %b %Y %H:%M")
                return dt.timestamp()
        except Exception:
            pass
    return 0 # Fallback for completely corrupt dates

def fetch_local_emails():
    target_inbox = "/home/ethanmoore/.thunderbird/5simsw9w.default-release/webaccountMail/outlook.cloud.microsoft/Inbox"

    if not os.path.exists(target_inbox):
        return [{"subject": "Waiting for sync...", "sender": "Status", "time": "Now"}]
    
    all_emails = []
    
    try:
        with open(target_inbox, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            
        # Split strictly by Unix mbox boundary
        messages = content.split("\nFrom ")
        
        for raw_msg in messages:
            if not raw_msg.strip():
                continue
                
            header_part = raw_msg.split("\n\n", 1)[0]
            
            # Check for Thunderbird's hard deletion flag
            status_match = re.search(r'^X-Mozilla-Status:\s*([0-9a-fA-F]+)', header_part, re.MULTILINE)
            if status_match:
                status = int(status_match.group(1), 16)
                if status & 0x0008: # If explicitly deleted, skip
                    continue

            # Extract fields safely using flexible regex
            sub_match = re.search(r'^Subject:\s*(.*?)$', header_part, re.MULTILINE | re.IGNORECASE)
            from_match = re.search(r'^From:\s*(.*?)$', header_part, re.MULTILINE | re.IGNORECASE)
            date_match = re.search(r'^Date:\s*(.*?)$', header_part, re.MULTILINE | re.IGNORECASE)
            
            subject = decode_header_text(sub_match.group(1)) if sub_match else "(No Subject)"
            sender = decode_header_text(from_match.group(1)) if from_match else "Unknown Sender"
            date_str = date_match.group(1).strip() if date_match else ""
            
            if not date_match or "Status" in sender:
                continue

            # Clean up display tags
            if "<" in sender:
                sender = sender.split("<")[0].strip()
            sender = sender.strip('"').strip("'")
            subject = subject.strip('"').strip("'")
            
            # Clean up tracking strings out of subjects
            subject = re.sub(r'=\?UTF-8\?[B|Q]\?(.*?)\?=', r'\1', subject)
            
            timestamp = parse_date_to_timestamp(date_str)
            
            # Format time display cleanly
            try:
                dt = email.utils.parsedate_to_datetime(date_str)
                display_time = dt.strftime("%d %b, %H:%M")
            except Exception:
                # If date parsing fails, extract just the day/month/time via text slice
                display_time = date_str[:16]

            all_emails.append({
                "subject": subject[:35],
                "sender": sender[:25],
                "timestamp": timestamp,
                "time": display_time
            })

        # Sort strictly by timestamp value
        all_emails.sort(key=lambda x: x["timestamp"], reverse=True)

        final_list = []
        for mail in all_emails[:5]:
            final_list.append({
                "subject": mail["subject"],
                "sender": mail["sender"],
                "time": mail["time"]
            })
            
        return final_list if final_list else [{"subject": "No emails processed", "sender": "Status", "time": "Now"}]

    except Exception as e:
        return [{"subject": f"Parser Error: {str(e)}", "sender": "Error", "time": "Now"}]

def main():
    home = os.path.expanduser("~")
    output_path = os.path.join(home, ".config/eww/emails.json")
    with open(output_path, "w") as f:
        json.dump(fetch_local_emails(), f, indent=4)

if __name__ == "__main__":
    main()