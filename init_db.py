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
    answer3 TEXT,
    correct3 INTEGER,
    answer4 TEXT,
    correct4 INTEGER,
    feedback TEXT
)
''')

# Clear existing data to avoid duplicates on re-running the script
c.execute('DELETE FROM questions')

sample_data = [
    # Category: Social Engineering (10 questions)
    ("social-engineering", "An attacker calls you pretending to be from IT support and asks for your password. What is this an example of?", "Vishing", 1, "A normal support call", 0, "Smishing", 0, "Pharming", 0, "Correct! Vishing is a form of social engineering that uses voice calls."),
    ("social-engineering", "Researching a target's personal and professional life on social media to create a convincing attack is called:", "Reconnaissance", 1, "Hacking", 0, "Socializing", 0, "Spamming", 0, "Correct! This information gathering is a key first step in social engineering."),
    ("social-engineering", "An email that creates a sense of panic to make you act without thinking is using which tactic?", "Urgency", 1, "Encryption", 0, "Authority", 0, "Curiosity", 0, "Correct! Attackers often use urgency to bypass rational thought."),
    ("social-engineering", "Gaining an employee's trust by pretending to be 'new in the office' and asking for help is a form of what?", "Impersonation", 1, "Networking", 0, "Onboarding", 0, "Mentoring", 0, "Correct! This is a classic impersonation tactic to gain unauthorized access."),
    ("social-engineering", "What is 'tailgating' in a physical security context?", "Following an authorized person into a secure area", 1, "Attending a company party", 0, "Setting up a security camera", 0, "Driving too close to a car", 0, "Correct! Tailgating is a physical social engineering technique to bypass security controls."),
    ("social-engineering", "An attacker offers a 'free USB drive' at a conference. What might be the risk?", "It could contain malware (Baiting)", 1, "The drive could be low quality", 0, "It might not be compatible", 0, "It's a marketing gift", 0, "Correct! This tactic, known as baiting, preys on curiosity or greed."),
    ("social-engineering", "The primary goal of social engineering is to:", "Manipulate people to divulge information", 1, "Break computer code", 0, "Install hardware", 0, "Improve social skills", 0, "Correct! Social engineering targets the 'human element' of security."),
    ("social-engineering", "Claiming to be a high-level executive to intimidate an employee into providing data is a tactic known as:", "Pretexting/Authority", 1, "Standard procedure", 0, "Delegation", 0, "Intimidation", 0, "Correct! Attackers use a believable story (pretext) and claims of authority."),
    ("social-engineering", "If you suspect someone is trying to social engineer you, what should you do?", "Verify their identity through a trusted, independent channel", 1, "Give them what they want to be helpful", 0, "Ignore them and hope they go away", 0, "Ask them for their ID", 0, "Correct! Always verify requests for sensitive information independently."),
    ("social-engineering", "Which human emotion is most commonly exploited by social engineers?", "Trust", 1, "Anger", 0, "Sadness", 0, "Joy", 0, "Correct! Building a sense of trust is fundamental to most social engineering attacks."),

    # Category: Phishing (10 questions)
    ("phishing", "You receive an email with a link to reset your password, but you didn't request it. What should you do?", "Delete it and report as phishing", 1, "Click the link to be safe", 0, "Reply to ask if it's real", 0, "Forward it to a friend", 0, "Correct! Unsolicited password reset links are a common phishing tactic."),
    ("phishing", "A major red flag in a phishing email is often:", "Generic greetings like 'Dear Valued Customer'", 1, "A company logo", 0, "Perfect grammar", 0, "An unsubscribe link", 0, "Correct! Legitimate companies usually address you by your name."),
    ("phishing", "What is 'Spear Phishing'?", "A phishing attack that is highly targeted", 1, "A phishing attack sent to millions of people", 0, "Phishing using a fishing pole icon", 0, "A phishing attack for fishermen", 0, "Correct! Spear phishing uses personalized information to seem more credible."),
    ("phishing", "What should you do if you hover your mouse over a link in an email and the URL shown is different from the link text?", "Do not click the link", 1, "Click the link to see where it goes", 0, "Copy the link and paste it in a new tab", 0, "Right-click and open in incognito", 0, "Correct! A mismatched URL is a strong indicator of a phishing attempt."),
    ("phishing", "Phishing attacks are only sent through email.", "False", 1, "True", 0, "Only on weekdays", 0, "Only in the morning", 0, "Correct! Phishing can also occur via text messages (Smishing), voice calls (Vishing), and social media."),
    ("phishing", "An email from a colleague asks you to buy gift cards for a client and send them the codes. This is likely:", "A Business Email Compromise (BEC) scam", 1, "A legitimate and urgent request", 0, "A team-building exercise", 0, "A new company policy", 0, "Correct! This is a common scam. Verify such requests in person or by a known phone number."),
    ("phishing", "Why do attackers use typos and grammatical errors in phishing emails?", "To bypass spam filters", 1, "Because they are not good at spelling", 0, "To make the email look more human", 0, "To test your attention to detail", 0, "Correct! Deliberate errors can sometimes evade filters looking for specific phrases."),
    ("phishing", "What is the primary danger of clicking a link in a phishing email?", "It can lead to malware or a fake login page", 1, "It will just show an advertisement", 0, "It will crash your email client", 0, "It will unsubscribe you from a list", 0, "Correct! The goal is to either infect your device or steal your credentials."),
    ("phishing", "Modern web browsers can help detect phishing sites.", "True", 1, "False", 0, "Only on secure networks", 0, "Only if you pay for a subscription", 0, "Correct! Many browsers have built-in filters that will warn you before visiting a known malicious website."),
    ("phishing", "If an email looks like it's from your CEO but the 'From' address is a public email service (like @gmail.com), you should be:", "Suspicious", 1, "Compliant", 0, "Impressed", 0, "Honored", 0, "Correct! An executive would almost always use their official company email address."),

    # Category: Vishing (10 questions)
    ("vishing", "What is the primary medium used in a vishing attack?", "Phone calls", 1, "Websites", 0, "Emails", 0, "Text messages", 0, "Correct! Vishing specifically refers to voice-based phishing."),
    ("vishing", "A scammer calls and says your computer is infected, then asks for remote access. This is a common:", "Tech support scam", 1, "Legitimate service", 0, "Computer diagnostic", 0, "Software update", 0, "Correct! Companies like Microsoft will not cold-call you about computer infections."),
    ("vishing", "The ability for scammers to make the caller ID show a legitimate number (like your bank's) is called:", "Caller ID Spoofing", 1, "Call Forwarding", 0, "Number Masking", 0, "Proxy Calling", 0, "Correct! Never trust caller ID alone to verify a caller's identity."),
    ("vishing", "If you receive an unexpected call from your 'bank' asking to 'verify' your full account number, what should you do?", "Hang up and call the bank's official number", 1, "Provide the information", 0, "Ask them to call you back later", 0, "Give them a fake number", 0, "Correct! Never provide sensitive data on a call you did not initiate."),
    ("vishing", "Vishing attacks often create a sense of _______ to manipulate you.", "Urgency or Fear", 1, "Calm", 0, "Joy", 0, "Trust", 0, "Correct! They might claim your account is locked or you're in trouble to make you act fast."),
    ("vishing", "What is an 'IVR' vishing attack?", "An automated voice system (IVR) that tricks you", 1, "A vishing attack from another country", 0, "A video-based vishing attack", 0, "An In-Vehicle Reconnaissance attack", 0, "Correct! Scammers use automated systems to trick users into typing their PINs or passwords."),
    ("vishing", "A caller claims you've won a lottery but need to pay a 'processing fee' first. This is a classic sign of:", "A scam", 1, "A real lottery win", 0, "A government tax", 0, "A handling charge", 0, "Correct! Legitimate lotteries do not require you to pay a fee to collect winnings."),
    ("vishing", "The term 'Vishing' is a combination of which two words?", "Voice and Phishing", 1, "Video and Fishing", 0, "Virtual and Phishing", 0, "Vocal and Fishing", 0, "Correct! It's phishing that happens over voice channels."),
    ("vishing", "If a vishing caller threatens you with legal action if you don't comply immediately, what is their goal?", "To scare you into acting without thinking", 1, "To provide legal advice", 0, "To serve you a real warrant", 0, "To help you avoid court", 0, "Correct! Threats are a high-pressure tactic used to cloud your judgment."),
    ("vishing", "The best defense against vishing is to be:", "Skeptical of unsolicited calls", 1, "Friendly to all callers", 0, "Always ready with your personal info", 0, "Quick to hang up on anyone", 0, "Correct! A healthy dose of skepticism is your best protection."),

    # Category: Smishing (10 questions)
    ("smishing", "You get a text message saying you've won a prize and need to click a link to claim it. This is likely:", "Smishing", 1, "A legitimate contest", 0, "A marketing promotion", 0, "A wrong number", 0, "Correct! Smishing is phishing conducted via SMS text messages."),
    ("smishing", "A text from a 'delivery service' with a tracking link for a package you didn't order is probably:", "A smishing attempt", 1, "A surprise gift", 0, "An error in their system", 0, "A package for a neighbor", 0, "Correct! Attackers use this lure to get you to click malicious links."),
    ("smishing", "What makes smishing dangerous?", "People tend to trust text messages more", 1, "Texts can't be traced", 0, "Texts are encrypted", 0, "All links in texts are safe", 0, "Correct! The personal and immediate nature of texts makes people lower their guard."),
    ("smishing", "A text message warns that your bank account has been suspended and asks you to call a number. You should:", "Call the official number on your bank card", 1, "Immediately call the number in the text", 0, "Text back asking for more info", 0, "Ignore the message completely", 0, "Correct! Never use contact information provided in a suspicious message."),
    ("smishing", "Smishing messages often contain what?", "A sense of urgency and a link", 1, "A personalized greeting card", 0, "A long, detailed explanation", 0, "A joke or a meme", 0, "Correct! The goal is to get you to click the link or call a number right away."),
    ("smishing", "Is it safe to reply 'STOP' to a suspicious text message?", "It can be risky; it confirms your number is active", 1, "Yes, it's always the safest option", 0, "Yes, it's required by law", 0, "No, it will infect your phone", 0, "Correct! While it often works for legitimate marketing, replying to a scammer just confirms they found a real person."),
    ("smishing", "The term 'Smishing' is a combination of which two words?", "SMS and Phishing", 1, "Smart and Phishing", 0, "Social and Phishing", 0, "Mobile and Fishing", 0, "Correct! It refers to phishing attacks delivered via SMS (Short Message Service)."),
    ("smishing", "A text from an unknown number has a photo and a generic message like 'Is this you?'. You should:", "Delete the message without clicking", 1, "Click the photo to see it clearly", 0, "Reply with 'Who is this?'", 0, "Forward it to your contacts", 0, "Correct! This is a common tactic to entice you to click a malicious link."),
    ("smishing", "If a smishing message asks for personal information, you should:", "Never provide it", 1, "Provide it if the message looks important", 0, "Only provide your name", 0, "Text them to call you instead", 0, "Correct! Legitimate organizations will not ask for sensitive data via text."),
    ("smishing", "Attackers can use your phone number for smishing if it was exposed in a:", "Data breach", 1, "Phone book", 0, "Your social media profile", 0, "A business card", 0, "Correct! Scammers buy lists of phone numbers from data breaches on the dark web."),

    # Category: Password Hygiene (10 questions)
    ("password-hygiene", "How often should you ideally change your main passwords?", "Every 3-6 months", 1, "Never", 0, "Every day", 0, "Once a year", 0, "Correct! Regular password changes are a key part of good password hygiene."),
    ("password-hygiene", "Is it safe to use the same password for multiple websites?", "No, it's very risky", 1, "Yes, it's easier to remember", 0, "Yes, if it's a strong password", 0, "Only for unimportant sites", 0, "Correct! If one site is breached, attackers can use that password to access your other accounts."),
    ("password-hygiene", "What is the best way to store many complex passwords?", "Use a secure password manager", 1, "Write them on a sticky note", 0, "Store them in a text file", 0, "Memorize all of them", 0, "Correct! Password managers securely store and encrypt your passwords."),
    ("password-hygiene", "'Password123' is an example of:", "Poor password hygiene", 1, "A strong starting point", 0, "A temporary password", 0, "A complex password", 0, "Correct! It's one of the most common and easily guessed passwords."),
    ("password-hygiene", "What is Two-Factor Authentication (2FA)?", "A second layer of security after your password", 1, "Using two different passwords", 0, "A password that is two words", 0, "Logging in two times", 0, "Correct! It adds a crucial second step, like a code sent to your phone."),
    ("password-hygiene", "You should avoid using _______ in your passwords.", "Personal information", 1, "Special characters", 0, "Numbers", 0, "Capital letters", 0, "Correct! Personal information is often public and easy for an attacker to guess."),
    ("password-hygiene", "When you are finished using a website, what is the best practice?", "Log out of your account", 1, "Just close the browser tab", 0, "Clear your browser history", 0, "Shut down the computer", 0, "Correct! Logging out prevents others from accessing your session, especially on a shared computer."),
    ("password-hygiene", "A website forces you to create a password that is exactly 8 characters long. This is:", "A sign of a poor security practice", 1, "A good security policy", 0, "Industry standard", 0, "The most secure method", 0, "Correct! A strong policy should allow for much longer passwords and not have a restrictive maximum length."),
    ("password-hygiene", "What should you do if a service you use announces a data breach?", "Change your password for that service immediately", 1, "Wait for them to fix the issue", 0, "Delete your account", 0, "Log in to see if your data was stolen", 0, "Correct! You should also change the password on any other sites where you used the same one."),
    ("password-hygiene", "Is it a good idea to let your web browser save your passwords?", "It's convenient but a password manager is more secure", 1, "It is the most secure method available", 0, "It's a requirement for most websites", 0, "Yes, browser security is unbreakable", 0, "Correct! While better than nothing, dedicated password managers offer stronger encryption and features."),

    # Category: Strong Password (10 questions)
    ("strong-password", "Which of the following is the strongest password?", "Y6&x@9z!Pq*2", 1, "password123", 0, "MyPassword", 0, "12345678", 0, "Correct! Strong passwords are long and use a mix of character types."),
    ("strong-password", "What is a key characteristic of a strong password?", "Length and Complexity", 1, "Being easy to remember", 0, "Using a real word", 0, "Having a pattern", 0, "Correct! Length is often considered the most important factor in password strength."),
    ("strong-password", "A 'passphrase' (e.g., 'CorrectHorseBatteryStaple') is often stronger than a complex, short password because it is:", "Significantly longer", 1, "Easier to type", 0, "More complex", 0, "More memorable", 0, "Correct! The sheer length of a passphrase makes it much harder to crack through brute force."),
    ("strong-password", "Why is 'P@$$w0rd' not as strong as it looks?", "It uses common and predictable substitutions", 1, "It contains a dictionary word", 0, "It is too short", 0, "It has no special characters", 0, "Correct! Cracking tools are programmed to check for these common substitutions (like '@' for 'a')."),
    ("strong-password", "A password like 'Tr0ub4dor&3' is an example of a password that is:", "Complex but short", 1, "Long but simple", 0, "A good passphrase", 0, "Very secure", 0, "Correct! While it has complexity, modern cracking can guess this quickly. Length is more important."),
    ("strong-password", "What is a 'brute-force' attack?", "Trying every possible character combination", 1, "Tricking someone into giving you their password", 0, "Stealing a password database", 0, "Using one common password on many accounts", 0, "Correct! Longer and more complex passwords make brute-force attacks take much longer."),
    ("strong-password", "Including your username in your password is:", "A bad idea, as it gives a clue to attackers", 1, "A good idea for memorization", 0, "A security requirement", 0, "A way to make it stronger", 0, "Correct! You should never mix your username and password."),
    ("strong-password", "Should a password be a common word found in a dictionary?", "No, these are vulnerable to dictionary attacks", 1, "Yes, if you add a number at the end", 0, "Yes, if it's a long word", 0, "No, because they are hard to spell", 0, "Correct! Dictionary attacks use word lists to rapidly guess passwords."),
    ("strong-password", "The minimum recommended password length in 2024 is generally:", "12-14 characters", 1, "6-8 characters", 0, "8-10 characters", 0, "Over 20 characters", 0, "Correct! As computing power increases, the recommended minimum length for passwords also increases."),
    ("strong-password", "Adding a space character to a password or passphrase can:", "Increase its complexity and strength", 1, "Make the password invalid", 0, "Decrease its strength", 0, "Not change its strength", 0, "Correct! If the system allows it, spaces are just another character that increases the effort to crack it."),

    # Category: Ransomware (10 questions)
    ("ransomware", "What type of malware encrypts your files and demands a payment to restore them?", "Ransomware", 1, "Spyware", 0, "Adware", 0, "Virus", 0, "Correct! Ransomware holds your data hostage for a ransom."),
    ("ransomware", "What is the single best defense against ransomware?", "Maintaining regular, offline backups", 1, "Paying the ransom quickly", 0, "Using a strong firewall", 0, "Having antivirus software", 0, "Correct! If you have a backup, you can restore your files without paying."),
    ("ransomware", "Should you pay the ransom demanded by an attacker?", "Security experts advise against it", 1, "Yes, it's the only way to get files back", 0, "Yes, but negotiate the price", 0, "Pay if the data is important", 0, "Correct! Paying encourages more attacks, and there's no guarantee you'll get your files back."),
    ("ransomware", "How is ransomware most commonly delivered?", "Through phishing emails", 1, "Through the computer's power cord", 0, "Via Bluetooth", 0, "Through software updates", 0, "Correct! Unwittingly opening a malicious file is a primary infection vector."),
    ("ransomware", "What is a 'decryption key' in the context of ransomware?", "A digital key that can unlock the files", 1, "A key on the keyboard", 0, "A physical USB key", 0, "The original file password", 0, "Correct! The attacker promises to provide this key in exchange for the ransom."),
    ("ransomware", "Can ransomware infect cloud-synced folders (like Dropbox or Google Drive)?", "Yes", 1, "No", 0, "Only if the cloud is hacked", 0, "Only if you share the folder", 0, "Correct! If the ransomware encrypts files on your local machine, those encrypted files will then be synced to the cloud."),
    ("ransomware", "What is 'double extortion' ransomware?", "When attackers both encrypt and steal your data", 1, "When the ransom amount is doubled", 0, "When two different gangs attack you", 0, "When you have to pay in two currencies", 0, "Correct! This puts extra pressure on the victim to pay."),
    ("ransomware", "A file on your computer is suddenly renamed to 'document.doc.encrypted'. This is a sign of:", "A ransomware attack", 1, "A normal file update", 0, "A file corruption error", 0, "A cloud sync issue", 0, "Correct! Ransomware often changes file extensions after encryption."),
    ("ransomware", "If you are infected with ransomware, the first step should be to:", "Disconnect the machine from the network", 1, "Restart the computer", 0, "Pay the ransom", 0, "Run antivirus scan", 0, "Correct! This can prevent the ransomware from spreading to other devices on the same network."),
    ("ransomware", "Ransomware-as-a-Service (RaaS) is:", "A business model where criminals lease ransomware", 1, "A protection service against ransomware", 0, "A government anti-ransomware tool", 0, "A type of insurance policy", 0, "Correct! RaaS has lowered the barrier to entry for committing ransomware attacks."),

    # Category: Spyware (10 questions)
    ("spyware", "What is the main purpose of spyware?", "To secretly gather information from your device", 1, "To display advertisements", 0, "To speed up your computer", 0, "To clean your hard drive", 0, "Correct! Spyware is designed to monitor your activity without your knowledge."),
    ("spyware", "A 'keylogger' is a type of spyware that specifically records:", "Your keystrokes", 1, "Your screen display", 0, "Your mouse movements", 0, "Your audio conversations", 0, "Correct! This allows attackers to capture passwords, messages, and other sensitive information."),
    ("spyware", "How might spyware get on your computer?", "Bundled with 'free' software", 1, "Through your monitor", 0, "From a dusty USB port", 0, "By overcharging your battery", 0, "Correct! This is a very common distribution method. Always be careful with freeware."),
    ("spyware", "What is a common sign your device might have spyware?", "Unexpected battery drain or high data usage", 1, "Faster performance", 0, "More free storage space", 0, "Longer battery life", 0, "Correct! Spyware running in the background consumes system resources."),
    ("spyware", "What is 'Adware'?", "Software that automatically displays ads", 1, "Hardware for your computer", 0, "A type of antivirus", 0, "Software to block ads", 0, "Correct! While less malicious than other spyware, it is often installed without consent and can be intrusive."),
    ("spyware", "Can spyware be installed on mobile phones?", "Yes, through malicious apps or links", 1, "No, mobile operating systems are immune", 0, "Only on Android phones", 0, "Only on iPhones", 0, "Correct! Mobile spyware is a significant threat and can monitor calls, texts, and location."),
    ("spyware", "Software that monitors your web browsing to sell your data to advertisers is a form of:", "Spyware", 1, "A search engine", 0, "A web browser", 0, "An internet service provider", 0, "Correct! This is a common function of many types of spyware and adware."),
    ("spyware", "The best tool to find and remove spyware from your computer is:", "Reputable anti-malware software", 1, "Your computer's file browser", 0, "The Windows registry editor", 0, "The task manager", 0, "Correct! These tools are specifically designed to detect and quarantine malicious software."),
    ("spyware", "Is it legal for companies to install spyware?", "Only with your explicit consent", 1, "Yes, anytime", 0, "No, it is always illegal", 0, "Only if they are a government agency", 0, "Correct! So-called 'legitimate' spyware is often found in monitoring software, but its use is ethically and legally complex."),
    ("spyware", "To reduce the risk of spyware, you should:", "Only download apps from official stores", 1, "Never use the internet", 0, "Click every link to test it", 0, "Use public Wi-Fi for all downloads", 0, "Correct! Avoiding unofficial app stores and suspicious downloads is a critical protective step.")
]

c.executemany('INSERT INTO questions (category, question, answer1, correct1, answer2, correct2, answer3, correct3, answer4, correct4, feedback) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', sample_data)
conn.commit()
conn.close()

print("Database initialized with 10 questions for each of the 8 categories, each with 4 options.")