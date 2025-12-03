import pandas as pd
import random
import string
import os

def generate_legitimate_urls(count=200):
    domains = [
        "google.com", "youtube.com", "facebook.com", "amazon.com", "wikipedia.org",
        "twitter.com", "instagram.com", "linkedin.com", "reddit.com", "netflix.com",
        "microsoft.com", "apple.com", "twitch.tv", "stackoverflow.com", "github.com",
        "pinterest.com", "adobe.com", "wordpress.org", "tumblr.com", "paypal.com",
        "dropbox.com", "vimeo.com", "flickr.com", "medium.com", "soundcloud.com",
        "spotify.com", "slack.com", "zoom.us", "salesforce.com", "oracle.com"
    ]
    
    paths = [
        "about", "contact", "products", "services", "blog", "news", "support",
        "help", "login", "signup", "profile", "settings", "dashboard", "search",
        "explore", "categories", "items", "articles", "docs", "api"
    ]
    
    urls = []
    for _ in range(count):
        domain = random.choice(domains)
        path = random.choice(paths)
        # 70% chance of having a path, 30% just domain
        if random.random() > 0.3:
            # 50% chance of having a sub-path
            if random.random() > 0.5:
                sub_path = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 8)))
                url = f"https://www.{domain}/{path}/{sub_path}"
            else:
                url = f"https://www.{domain}/{path}"
        else:
            url = f"https://www.{domain}"
        urls.append(url)
    
    return urls

def generate_phishing_urls(count=200):
    targets = ["paypal", "google", "facebook", "apple", "amazon", "netflix", "bank", "secure", "login", "account"]
    tlds = [".com", ".net", ".org", ".tk", ".ml", ".ga", ".cf", ".gq", ".xyz", ".info"]
    
    urls = []
    for _ in range(count):
        target = random.choice(targets)
        method = random.choice(["typo", "subdomain", "ip", "hyphen"])
        
        if method == "typo":
            # Typosquatting: e.g., paypa1.com
            typo_target = target.replace('l', '1').replace('o', '0').replace('e', '3').replace('a', '@')
            if typo_target == target: # fallback if no replacements made
                typo_target = target + "1"
            url = f"http://{typo_target}{random.choice(tlds)}/login"
            
        elif method == "subdomain":
            # Suspicious subdomain: e.g., paypal.secure-update.com
            base = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
            url = f"http://{target}.{base}{random.choice(tlds)}/verify"
            
        elif method == "ip":
            # IP address URL
            ip = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
            url = f"http://{ip}/{target}/login"
            
        elif method == "hyphen":
            # Excessive hyphens: e.g., secure-login-paypal-update.com
            words = [target, "secure", "login", "update", "verify", "account"]
            random.shuffle(words)
            domain = "-".join(words[:3])
            url = f"https://{domain}{random.choice(tlds)}"
            
        urls.append(url)
    
    return urls

    return urls

def generate_legitimate_emails(count=200):
    templates = [
        "Hi Team,\nJust a reminder about the {event} tomorrow at {time}. See you there.\nBest,\n{name}",
        "Dear Customer,\nYour order #{order_id} has been shipped. Track it here: https://www.shipping.com/track/{order_id}\nThanks,\nSupport",
        "Hello,\nPlease find attached the agenda for the upcoming meeting regarding {topic}.\nRegards,\n{name}",
        "Hi {name},\nCan we reschedule our call to {time}? Let me know if that works.\nThanks,\n{sender}",
        "Weekly Newsletter: Check out our latest updates on {topic}. Read more at https://www.company.com/blog\nUnsubscribe if you wish.",
        "Your monthly statement for {month} is ready. Log in to your account to view it.\nhttps://www.bank.com/login",
        "Welcome to the team! We are excited to have you on board. Please review the attached handbook.\nHR Team",
        "Project Update: The {topic} phase is complete. We are moving to the next stage.\nBest,\nProject Manager"
    ]
    
    events = ["weekly sync", "project review", "all-hands meeting", "design sprint", "budget planning"]
    topics = ["Q4 goals", "new marketing strategy", "product launch", "security protocols", "holiday schedule"]
    names = ["John", "Sarah", "Mike", "Emily", "David", "Lisa", "Tom", "Anna"]
    times = ["10 AM", "2 PM", "11:30 AM", "4 PM", "9 AM"]
    months = ["January", "February", "March", "April", "May", "June"]
    
    emails = []
    for _ in range(count):
        template = random.choice(templates)
        content = template.format(
            event=random.choice(events),
            time=random.choice(times),
            name=random.choice(names),
            sender=random.choice(names),
            order_id=random.randint(10000, 99999),
            topic=random.choice(topics),
            month=random.choice(months)
        )
        emails.append(content.replace("\n", " ")) # Flatten for CSV
    
    return emails

def generate_phishing_emails(count=200):
    templates = [
        "URGENT: Your account has been compromised! Click here immediately to verify your identity: {link}",
        "CONGRATULATIONS! You have won a {prize}! Claim it now at {link} before it expires!",
        "Final Notice: Your invoice #{invoice_id} is overdue. Pay now to avoid legal action. View invoice: {link}",
        "Security Alert: Unusual sign-in activity detected. If this wasn't you, secure your account: {link}",
        "Dear User, your password expires in 24 hours. Update it here: {link}",
        "HR: Please review the attached document regarding your salary adjustment immediately. {link}",
        "Netflix: Your payment failed. Update your billing information to keep watching. {link}",
        "PayPal: You sent $500.00 USD to Unknown. If this wasn't you, cancel the transaction: {link}"
    ]
    
    prizes = ["iPhone 15", "$1000 Gift Card", "Luxury Vacation", "New Car", "Cash Prize"]
    links = [
        "http://paypal-secure-login.com", "http://verify-account-now.tk", "http://apple-id-reset.info",
        "http://bank-security-alert.xyz", "http://netflix-billing-update.net", "http://hr-portal-secure.com",
        "http://claim-prize-winner.com", "http://secure-login-attempt.org"
    ]
    
    emails = []
    for _ in range(count):
        template = random.choice(templates)
        content = template.format(
            prize=random.choice(prizes),
            link=random.choice(links),
            invoice_id=random.randint(1000, 9999)
        )
        emails.append(content.replace("\n", " ")) # Flatten for CSV
    
    return emails

def main():
    print("Generating synthetic data...")
    
    # URLs
    legit_urls = generate_legitimate_urls(200)
    phishing_urls = generate_phishing_urls(200)
    
    # Emails
    legit_emails = generate_legitimate_emails(200)
    phishing_emails = generate_phishing_emails(200)
    
    print(f"Generated {len(legit_urls)} legitimate URLs and {len(phishing_urls)} phishing URLs.")
    print(f"Generated {len(legit_emails)} legitimate emails and {len(phishing_emails)} phishing emails.")
    
    # Paths
    legit_path = "../data/legitimate_urls.csv"
    phishing_path = "../data/phishing_urls.csv"
    emails_path = "../data/emails.csv"
    
    # --- URLs ---
    if os.path.exists(legit_path):
        legit_df = pd.read_csv(legit_path)
    else:
        legit_df = pd.DataFrame(columns=['url', 'label'])
        
    if os.path.exists(phishing_path):
        phishing_df = pd.read_csv(phishing_path)
    else:
        phishing_df = pd.DataFrame(columns=['url', 'label'])
    
    new_legit_df = pd.DataFrame({'url': legit_urls, 'label': 0})
    new_phishing_df = pd.DataFrame({'url': phishing_urls, 'label': 1})
    
    updated_legit_df = pd.concat([legit_df, new_legit_df], ignore_index=True).drop_duplicates(subset=['url'])
    updated_phishing_df = pd.concat([phishing_df, new_phishing_df], ignore_index=True).drop_duplicates(subset=['url'])
    
    updated_legit_df.to_csv(legit_path, index=False)
    updated_phishing_df.to_csv(phishing_path, index=False)
    
    print(f"Updated {legit_path}: {len(updated_legit_df)} total rows.")
    print(f"Updated {phishing_path}: {len(updated_phishing_df)} total rows.")

    # --- Emails ---
    if os.path.exists(emails_path):
        emails_df = pd.read_csv(emails_path)
    else:
        emails_df = pd.DataFrame(columns=['content', 'label'])
        
    new_legit_emails_df = pd.DataFrame({'content': legit_emails, 'label': 0})
    new_phishing_emails_df = pd.DataFrame({'content': phishing_emails, 'label': 1})
    
    updated_emails_df = pd.concat([emails_df, new_legit_emails_df, new_phishing_emails_df], ignore_index=True).drop_duplicates(subset=['content'])
    updated_emails_df.to_csv(emails_path, index=False)
    
    print(f"Updated {emails_path}: {len(updated_emails_df)} total rows.")

if __name__ == "__main__":
    main()
