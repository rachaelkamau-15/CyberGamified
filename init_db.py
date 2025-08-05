# File: init_db.py
import sqlite3

conn = sqlite3.connect('questions.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    question TEXT,
    answer1 TEXT,
    correct1 INTEGER,
    answer2 TEXT,
    correct2 INTEGER,
    feedback TEXT
)
''')

# Clear existing data to avoid duplicates on re-running the script
c.execute('DELETE FROM questions')

sample_data = [
    # Category: Social Engineering (10 questions)
    ("social-engineering", "An attacker calls you pretending to be from IT support and asks for your password. What is this an example of?", "Vishing", 1, "A normal support call", 0, "Correct! Vishing is a form of social engineering that uses voice calls."),
    ("social-engineering", "Researching a target's personal and professional life on social media to create a convincing attack is called:", "Reconnaissance", 1, "Hacking", 0, "Correct! This information gathering is a key first step in social engineering."),
    ("social-engineering", "An email that creates a sense of panic to make you act without thinking is using which tactic?", "Urgency", 1, "Encryption", 0, "Correct! Attackers often use urgency to bypass rational thought."),
    ("social-engineering", "Gaining an employee's trust by pretending to be 'new in the office' and asking for help is a form of what?", "Impersonation", 1, "Networking", 0, "Correct! This is a classic impersonation tactic to gain unauthorized access."),
    ("social-engineering", "What is 'tailgating' in a physical security context?", "Following an authorized person into a secure area", 1, "Attending a company party", 0, "Correct! Tailgating is a physical social engineering technique to bypass security controls."),
    ("social-engineering", "An attacker offers a 'free USB drive' at a conference. What might be the risk?", "It could contain malware (Baiting)", 1, "The drive could be low quality", 0, "Correct! This tactic, known as baiting, preys on curiosity or greed."),
    ("social-engineering", "The primary goal of social engineering is to:", "Manipulate people to divulge information", 1, "Break computer code", 0, "Correct! Social engineering targets the 'human element' of security."),
    ("social-engineering", "Claiming to be a high-level executive to intimidate an employee into providing data is a tactic known as:", "Pretexting/Authority", 1, "Standard procedure", 0, "Correct! Attackers use a believable story (pretext) and claims of authority."),
    ("social-engineering", "If you suspect someone is trying to social engineer you, what should you do?", "Verify their identity through a trusted, independent channel", 1, "Give them what they want to be helpful", 0, "Correct! Always verify requests for sensitive information independently."),
    ("social-engineering", "Which human emotion is most commonly exploited by social engineers?", "Trust", 1, "Anger", 0, "Correct! Building a sense of trust is fundamental to most social engineering attacks."),

    # Category: Phishing (10 questions)
    ("phishing", "You receive an email with a link to reset your password, but you didn't request it. What should you do?", "Delete it and report as phishing", 1, "Click the link to be safe", 0, "Correct! Unsolicited password reset links are a common phishing tactic."),
    ("phishing", "A major red flag in a phishing email is often:", "Generic greetings like 'Dear Valued Customer'", 1, "A company logo", 0, "Correct! Legitimate companies usually address you by your name."),
    ("phishing", "What is 'Spear Phishing'?", "A phishing attack that is highly targeted at a specific individual or organization", 1, "A phishing attack sent to millions of people", 0, "Correct! Spear phishing uses personalized information to seem more credible."),
    ("phishing", "What should you do if you hover your mouse over a link in an email and the URL shown is different from the link text?", "Do not click the link", 1, "Click the link to see where it goes", 0, "Correct! A mismatched URL is a strong indicator of a phishing attempt."),
    ("phishing", "Phishing attacks are only sent through email.", "False", 1, "True", 0, "Correct! Phishing can also occur via text messages (Smishing), voice calls (Vishing), and social media."),
    ("phishing", "An email from a colleague asks you to buy gift cards for a client and send them the codes. This is likely:", "A Business Email Compromise (BEC) scam", 1, "A legitimate and urgent request", 0, "Correct! This is a common scam. Verify such requests in person or by a known phone number."),
    ("phishing", "Why do attackers use typos and grammatical errors in phishing emails?", "To bypass spam filters", 1, "Because they are not good at spelling", 0, "Correct! Deliberate errors can sometimes evade filters looking for specific phrases."),
    ("phishing", "What is the primary danger of clicking a link in a phishing email?", "It can lead to malware installation or a fake login page", 1, "It will just show an advertisement", 0, "Correct! The goal is to either infect your device or steal your credentials."),
    ("phishing", "Modern web browsers can help detect phishing sites.", "True", 1, "False", 0, "Correct! Many browsers have built-in filters that will warn you before visiting a known malicious website."),
    ("phishing", "If an email looks like it's from your CEO but the 'From' address is a public email service (like @gmail.com), you should be:", "Suspicious", 1, "Compliant", 0, "Correct! An executive would almost always use their official company email address."),

    # Category: Vishing (10 questions)
    ("vishing", "What is the primary medium used in a vishing attack?", "Phone calls", 1, "Websites", 0, "Correct! Vishing specifically refers to voice-based phishing."),
    ("vishing", "A scammer calls and says your computer is infected, then asks for remote access. This is a common:", "Tech support scam", 1, "Legitimate service", 0, "Correct! Companies like Microsoft will not cold-call you about computer infections."),
    ("vishing", "The ability for scammers to make the caller ID show a legitimate number (like your bank's) is called:", "Caller ID Spoofing", 1, "Call Forwarding", 0, "Correct! Never trust caller ID alone to verify a caller's identity."),
    ("vishing", "If you receive an unexpected call from your 'bank' asking to 'verify' your full account number, what should you do?", "Hang up and call the bank's official number", 1, "Provide the information", 0, "Correct! Never provide sensitive data on a call you did not initiate."),
    ("vishing", "Vishing attacks often create a sense of _______ to manipulate you.", "Urgency or Fear", 1, "Calm", 0, "Correct! They might claim your account is locked or you're in trouble to make you act fast."),
    ("vishing", "What is an 'IVR' vishing attack?", "An automated voice system (IVR) that tricks you into entering data", 1, "A vishing attack from another country", 0, "Correct! Scammers use automated systems to trick users into typing their PINs or passwords."),
    ("vishing", "A caller claims you've won a lottery but need to pay a 'processing fee' first. This is a classic sign of:", "A scam", 1, "A real lottery win", 0, "Correct! Legitimate lotteries do not require you to pay a fee to collect winnings."),
    ("vishing", "The term 'Vishing' is a combination of which two words?", "Voice and Phishing", 1, "Video and Fishing", 0, "Correct! It's phishing that happens over voice channels."),
    ("vishing", "If a vishing caller threatens you with legal action if you don't comply immediately, what is their goal?", "To scare you into acting without thinking", 1, "To provide legal advice", 0, "Correct! Threats are a high-pressure tactic used to cloud your judgment."),
    ("vishing", "The best defense against vishing is to be:", "Skeptical of unsolicited calls", 1, "Friendly to all callers", 0, "Correct! A healthy dose of skepticism is your best protection."),

    # Category: Smishing (10 questions)
    ("smishing", "You get a text message saying you've won a prize and need to click a link to claim it. This is likely:", "Smishing", 1, "A legitimate contest", 0, "Correct! Smishing is phishing conducted via SMS text messages."),
    ("smishing", "A text from a 'delivery service' with a tracking link for a package you didn't order is probably:", "A smishing attempt", 1, "A surprise gift", 0, "Correct! Attackers use this lure to get you to click malicious links."),
    ("smishing", "What makes smishing dangerous?", "People tend to trust text messages more than emails", 1, "Texts can't be traced", 0, "Correct! The personal and immediate nature of texts makes people lower their guard."),
    ("smishing", "A text message warns that your bank account has been suspended and asks you to call a number. You should:", "Call the official number on your bank card", 1, "Immediately call the number in the text", 0, "Correct! Never use contact information provided in a suspicious message."),
    ("smishing", "Smishing messages often contain what?", "A sense of urgency and a link", 1, "A personalized greeting card", 0, "Correct! The goal is to get you to click the link or call a number right away."),
    ("smishing", "Is it safe to reply 'STOP' to a suspicious text message?", "It can be risky; it confirms your number is active", 1, "Yes, it's always the safest option", 0, "Correct! While it often works for legitimate marketing, replying to a scammer just confirms they found a real person."),
    ("smishing", "The term 'Smishing' is a combination of which two words?", "SMS and Phishing", 1, "Smart and Phishing", 0, "Correct! It refers to phishing attacks delivered via SMS (Short Message Service)."),
    ("smishing", "A text from an unknown number has a photo and a generic message like 'Is this you?'. You should:", "Delete the message without clicking", 1, "Click the photo to see it clearly", 0, "Correct! This is a common tactic to entice you to click a malicious link."),
    ("smishing", "If a smishing message asks for personal information, you should:", "Never provide it", 1, "Provide it if the message looks important", 0, "Correct! Legitimate organizations will not ask for sensitive data via text."),
    ("smishing", "Attackers can use your phone number for smishing if it was exposed in a:", "Data breach", 1, "Phone book", 0, "Correct! Scammers buy lists of phone numbers from data breaches on the dark web."),

    # Category: Password Hygiene (10 questions)
    ("password-hygiene", "How often should you ideally change your main passwords?", "Every 3-6 months", 1, "Never", 0, "Correct! Regular password changes are a key part of good password hygiene."),
    ("password-hygiene", "Is it safe to use the same password for multiple websites?", "No, it's very risky", 1, "Yes, it's easier to remember", 0, "Correct! If one site is breached, attackers can use that password to access your other accounts."),
    ("password-hygiene", "What is the best way to store many complex passwords?", "Use a secure password manager", 1, "Write them on a sticky note", 0, "Correct! Password managers securely store and encrypt your passwords."),
    ("password-hygiene", "'Password123' is an example of:", "Poor password hygiene", 1, "A strong starting point", 0, "Correct! It's one of the most common and easily guessed passwords."),
    ("password-hygiene", "What is Two-Factor Authentication (2FA)?", "A second layer of security after your password", 1, "Using two different passwords", 0, "Correct! It adds a crucial second step, like a code sent to your phone."),
    ("password-hygiene", "You should avoid using _______ in your passwords.", "Personal information (e.g., your birthday)", 1, "Special characters", 0, "Correct! Personal information is often public and easy for an attacker to guess."),
    ("password-hygiene", "When you are finished using a website, what is the best practice?", "Log out of your account", 1, "Just close the browser tab", 0, "Correct! Logging out prevents others from accessing your session, especially on a shared computer."),
    ("password-hygiene", "A website forces you to create a password that is exactly 8 characters long. This is:", "A sign of a poor security practice", 1, "A good security policy", 0, "Correct! A strong policy should allow for much longer passwords and not have a restrictive maximum length."),
    ("password-hygiene", "What should you do if a service you use announces a data breach?", "Change your password for that service immediately", 1, "Wait for them to fix the issue", 0, "Correct! You should also change the password on any other sites where you used the same one."),
    ("password-hygiene", "Is it a good idea to let your web browser save your passwords?", "It's convenient but a password manager is more secure", 1, "It is the most secure method available", 0, "Correct! While better than nothing, dedicated password managers offer stronger encryption and features."),

    # Category: Strong Password (10 questions)
    ("strong-password", "Which of the following is the strongest password?", "Y6&x@9z!Pq*2", 1, "password123", 0, "Correct! Strong passwords are long and use a mix of character types."),
    ("strong-password", "What is a key characteristic of a strong password?", "Length and Complexity", 1, "Being easy to remember", 0, "Correct! Length is often considered the most important factor in password strength."),
    ("strong-password", "A 'passphrase' (e.g., 'CorrectHorseBatteryStaple') is often stronger than a complex, short password because it is:", "Significantly longer", 1, "Easier to type", 0, "Correct! The sheer length of a passphrase makes it much harder to crack through brute force."),
    ("strong-password", "Why is 'P@$$w0rd' not as strong as it looks?", "It uses common and predictable character substitutions", 1, "It contains a dictionary word", 0, "Correct! Cracking tools are programmed to check for these common substitutions (like '@' for 'a')."),
    ("strong-password", "A password like 'Tr0ub4dor&3' is an example of a password that is:", "Complex but short", 1, "Long but simple", 0, "Correct! While it has complexity, modern cracking can guess this quickly. Length is more important."),
    ("strong-password", "What is a 'brute-force' attack?", "Trying every possible combination of characters to guess a password", 1, "Tricking someone into giving you their password", 0, "Correct! Longer and more complex passwords make brute-force attacks take much longer."),
    ("strong-password", "Including your username in your password is:", "A bad idea, as it gives a clue to attackers", 1, "A good idea for memorization", 0, "Correct! You should never mix your username and password."),
    ("strong-password", "Should a password be a common word found in a dictionary?", "No, these are vulnerable to dictionary attacks", 1, "Yes, if you add a number at the end", 0, "Correct! Dictionary attacks use word lists to rapidly guess passwords."),
    ("strong-password", "The minimum recommended password length in 2024 is generally:", "12-14 characters", 1, "6-8 characters", 0, "Correct! As computing power increases, the recommended minimum length for passwords also increases."),
    ("strong-password", "Adding a space character to a password or passphrase can:", "Increase its complexity and strength", 1, "Make the password invalid", 0, "Correct! If the system allows it, spaces are just another character that increases the effort to crack it."),

    # Category: Ransomware (10 questions)
    ("ransomware", "What type of malware encrypts your files and demands a payment to restore them?", "Ransomware", 1, "Spyware", 0, "Correct! Ransomware holds your data hostage for a ransom."),
    ("ransomware", "What is the single best defense against ransomware?", "Maintaining regular, offline backups of your data", 1, "Paying the ransom quickly", 0, "Correct! If you have a backup, you can restore your files without paying."),
    ("ransomware", "Should you pay the ransom demanded by an attacker?", "Security experts advise against it", 1, "Yes, it's the only way to get files back", 0, "Correct! Paying encourages more attacks, and there's no guarantee you'll get your files back."),
    ("ransomware", "How is ransomware most commonly delivered?", "Through phishing emails with malicious attachments or links", 1, "Through the computer's power cord", 0, "Correct! Unwittingly opening a malicious file is a primary infection vector."),
    ("ransomware", "What is a 'decryption key' in the context of ransomware?", "A digital key that can unlock the encrypted files", 1, "A key on the keyboard", 0, "Correct! The attacker promises to provide this key in exchange for the ransom."),
    ("ransomware", "Can ransomware infect cloud-synced folders (like Dropbox or Google Drive)?", "Yes", 1, "No", 0, "Correct! If the ransomware encrypts files on your local machine, those encrypted files will then be synced to the cloud."),
    ("ransomware", "What is 'double extortion' ransomware?", "When attackers both encrypt and steal your data, threatening to leak it", 1, "When the ransom amount is doubled", 0, "Correct! This puts extra pressure on the victim to pay."),
    ("ransomware", "A file on your computer is suddenly renamed to 'document.doc.encrypted'. This is a sign of:", "A ransomware attack", 1, "A normal file update", 0, "Correct! Ransomware often changes file extensions after encryption."),
    ("ransomware", "If you are infected with ransomware, the first step should be to:", "Disconnect the infected machine from the network", 1, "Restart the computer", 0, "Correct! This can prevent the ransomware from spreading to other devices on the same network."),
    ("ransomware", "Ransomware-as-a-Service (RaaS) is:", "A business model where ransomware creators lease their tools to other criminals", 1, "A protection service against ransomware", 0, "Correct! RaaS has lowered the barrier to entry for committing ransomware attacks."),

    # Category: Spyware (10 questions)
    ("spyware", "What is the main purpose of spyware?", "To secretly gather information from your device", 1, "To display advertisements", 0, "Correct! Spyware is designed to monitor your activity without your knowledge."),
    ("spyware", "A 'keylogger' is a type of spyware that specifically records:", "Your keystrokes", 1, "Your screen display", 0, "Correct! This allows attackers to capture passwords, messages, and other sensitive information."),
    ("spyware", "How might spyware get on your computer?", "Bundled with 'free' software you download", 1, "Through your monitor", 0, "Correct! This is a very common distribution method. Always be careful with freeware."),
    ("spyware", "What is a common sign your device might have spyware?", "Unexpected battery drain or high data usage", 1, "Faster performance", 0, "Correct! Spyware running in the background consumes system resources."),
    ("spyware", "What is 'Adware'?", "Software that automatically displays or downloads advertisements", 1, "Hardware for your computer", 0, "Correct! While less malicious than other spyware, it is often installed without consent and can be intrusive."),
    ("spyware", "Can spyware be installed on mobile phones?", "Yes, through malicious apps or links", 1, "No, mobile operating systems are immune", 0, "Correct! Mobile spyware is a significant threat and can monitor calls, texts, and location."),
    ("spyware", "Software that monitors your web browsing to sell your data to advertisers is a form of:", "Spyware", 1, "A search engine", 0, "Correct! This is a common function of many types of spyware and adware."),
    ("spyware", "The best tool to find and remove spyware from your computer is:", "Reputable anti-malware software", 1, "Your computer's file browser", 0, "Correct! These tools are specifically designed to detect and quarantine malicious software."),
    ("spyware", "Is it legal for companies to install spyware?", "Only with your explicit consent (often buried in a user agreement)", 1, "Yes, anytime", 0, "Correct! So-called 'legitimate' spyware is often found in monitoring software, but its use is ethically and legally complex."),
    ("spyware", "To reduce the risk of spyware, you should:", "Only download apps from official stores and trusted sources", 1, "Never use the internet", 0, "Correct! Avoiding unofficial app stores and suspicious downloads is a critical protective step.")
]

c.executemany('INSERT INTO questions (category, question, answer1, correct1, answer2, correct2, feedback) VALUES (?, ?, ?, ?, ?, ?, ?)', sample_data)
conn.commit()
conn.close()

print("Database initialized with 10 questions for each of the 8 categories.")