import sqlite3

# =========================================================================
#                             SAMPLE QUESTIONS
# =========================================================================
# 10 questions for each of the 8 categories.
sample_questions = [
    # --- Category: Phishing (10 questions) ---
    ('phishing', 'You receive an email from "Amaz0n" about a suspicious login. What is the biggest red flag?', 'The link asks you to verify credit card details.', 0, 'The sender\'s email address is slightly misspelled.', 1, 'The email uses the official Amazon logo.', 0, 'It was sent in the middle of the night.', 0, 'Correct! Misspelled sender addresses are a classic phishing tactic.'),
    ('phishing', 'A phishing email often tries to create a sense of...', 'Calm and relaxation', 0, 'Urgency or fear', 1, 'Curiosity and excitement', 0, 'Confusion', 0, 'Correct! Attackers want you to act quickly without thinking, so they use urgent language like "Account will be suspended".'),
    ('phishing', 'What should you do if you receive a suspicious email with an attachment you weren\'t expecting?', 'Open the attachment to see what it is.', 0, 'Reply and ask if they meant to send it.', 0, 'Delete the email immediately without opening the attachment.', 1, 'Forward it to your IT department\'s public email.', 0, 'Correct! Unexpected attachments can contain malware. It is safest to delete the email entirely.'),
    ('phishing', 'Which of these is a "generic greeting" often used in phishing scams?', '"Dear John Smith,"', 0, '"Hi [Your Username],"', 0, '"Dear Valued Customer,"', 1, '"Regarding your recent order,"', 0, 'Correct! Legitimate companies will usually address you by your actual name, not a generic title.'),
    ('phishing', 'Hovering your mouse over a link in an email without clicking it can help you...', 'Download the linked file safely.', 0, 'See the actual web address the link points to.', 1, 'Determine if the sender is in your contacts.', 0, 'Translate the link into another language.', 0, 'Correct! The actual destination URL often appears in the bottom corner of your browser, revealing if it leads to a suspicious site.'),
    ('phishing', 'Your bank sends an email asking you to "click here to update your security questions." This is most likely...', 'A standard security procedure.', 0, 'A phishing attempt to steal your login credentials.', 1, 'A new feature announcement.', 0, 'A required regulatory update.', 0, 'Correct! Banks will almost never ask you to update sensitive information via a direct email link.'),
    ('phishing', 'Phishing can only happen through email.', 'True', 0, 'False', 1, 'Only on weekdays', 0, 'Only from foreign countries', 0, 'Correct! False. Phishing also occurs via text messages (Smishing) and voice calls (Vishing).'),
    ('phishing', 'What does the "S" in "HTTPS" at the beginning of a URL stand for?', 'Safe', 0, 'Standard', 0, 'Secure', 1, 'Special', 0, 'Correct! It means the connection to the website is encrypted and secure, though phishing sites can sometimes still use it.'),
    ('phishing', 'An email says you\'ve won a lottery you never entered. What should you do?', 'Reply with your bank details to claim the prize.', 0, 'Click the link to see the prize details.', 0, 'Share the good news on social media.', 0, 'Recognize it as a scam and delete it.', 1, 'Correct! "You\'ve won" scams are a very common way to trick people into giving away personal information or money.'),
    ('phishing', 'If you accidentally click on a phishing link, what is the first thing you should do?', 'Immediately shut down your computer.', 0, 'Change the password for that account and any other accounts using the same password.', 1, 'Wait to see if anything bad happens.', 0, 'Unplug your router.', 0, 'Correct! Immediately changing your passwords can prevent attackers from using any credentials you may have exposed.'),

    # --- Category: Social Engineering (10 questions) ---
    ('social-engineering', 'What is the primary goal of social engineering?', 'To find bugs in software.', 0, 'To manipulate people into divulging confidential information.', 1, 'To install hardware keyloggers.', 0, 'To physically break into a building.', 0, 'Correct! Social engineering relies on psychological manipulation rather than technical hacking.'),
    ('social-engineering', 'An attacker finds your personal details on social media to guess your password. This technique is known as:', 'Phishing', 0, 'Baiting', 0, 'Pretexting', 0, 'Information Gathering', 1, 'Correct! Attackers gather information from public sources to make their attacks more believable or to guess credentials.'),
    ('social-engineering', 'Leaving a malware-infected USB drive in a company parking lot for an employee to find and plug in is an example of:', 'Baiting', 1, 'Tailgating', 0, 'Quid pro quo', 0, 'Phishing', 0, 'Correct! Baiting preys on human curiosity by offering something enticing to trick a victim into exposing their system.'),
    ('social-engineering', 'An attacker calls you pretending to be a colleague who needs your password to finish an "urgent project." This is an example of:', 'Pretexting', 1, 'Spyware', 0, 'Ransomware', 0, 'Diversion theft', 0, 'Correct! Pretexting involves creating a fabricated scenario (a pretext) to gain the victim\'s trust.'),
    ('social-engineering', 'Following an authorized person into a secure area without their knowledge is called:', 'Piggybacking', 0, 'Baiting', 0, 'Shoulder Surfing', 0, 'Tailgating', 1, 'Correct! Tailgating is the act of physically following an authorized person through a secure checkpoint.'),
    ('social-engineering', 'An attacker offers you a free movie download in exchange for your login credentials. This is known as:', 'Quid pro quo', 1, 'Watering hole', 0, 'Pretexting', 0, 'Scareware', 0, 'Correct! Quid pro quo means "something for something," where an attacker offers a benefit in exchange for information.'),
    ('social-engineering', 'Looking over someone\'s shoulder to see them type in their password is known as:', 'Tailgating', 0, 'Shoulder Surfing', 1, 'Eavesdropping', 0, 'Baiting', 0, 'Correct! Shoulder surfing is a simple but effective direct observation technique.'),
    ('social-engineering', 'The strongest defense against social engineering is:', 'A strong firewall.', 0, 'Up-to-date antivirus software.', 0, 'A culture of security awareness and a healthy sense of skepticism.', 1, 'Complex passwords.', 0, 'Correct! Since social engineering targets humans, awareness and critical thinking are the best defenses.'),
    ('social-engineering', 'Why is social engineering so effective?', 'It uses advanced hacking tools.', 0, 'It targets the most vulnerable part of any system: the human element.', 1, 'It only works on non-technical people.', 0, 'It is always done in person.', 0, 'Correct! People are often easier to trick than computer systems are to hack.'),
    ('social-engineering', 'An email from your CEO asks you to urgently transfer money to a new vendor account. What should you do first?', 'Transfer the money immediately as requested.', 0, 'Reply to the email to confirm the details.', 0, 'Verbally confirm the request with the CEO or their assistant through a trusted channel (like a phone call).', 1, 'Forward the email to the finance department.', 0, 'Correct! This could be a Business Email Compromise (BEC) attack. Always verify unusual financial requests out-of-band (i.e., not by replying to the email).'),

    # --- Category: Vishing (10 questions) ---
    ('vishing', 'What does "Vishing" stand for?', 'Video Phishing', 0, 'Virus Phishing', 0, 'Voice Phishing', 1, 'Virtual Phishing', 0, 'Correct! Vishing uses voice communication, like phone calls or voicemails, to conduct phishing attacks.'),
    ('vishing', 'You receive an automated call from your "bank" saying your account is frozen and you must press 1 to speak to an agent. This is likely...', 'A vishing attack.', 1, 'A standard bank procedure.', 0, 'A wrong number.', 0, 'A marketing call.', 0, 'Correct! Banks rarely use automated calls for urgent security issues. This is a common vishing tactic.'),
    ('vishing', 'The best way to verify a suspicious call from your credit card company is to:', 'Call them back using the number they provide on the call.', 0, 'Give them your personal information to confirm your identity.', 0, 'Hang up and call the number on the back of your credit card.', 1, 'Ask them to prove who they are.', 0, 'Correct! Always use a trusted, official number to verify a request, never a number provided by the caller.'),
    ('vishing', 'Vishing attackers often use technology to make the caller ID show a legitimate number (e.g., your bank\'s). This is called:', 'ID Masking', 0, 'Caller ID Spoofing', 1, 'Number Cloning', 0, 'Phone Hijacking', 0, 'Correct! Caller ID spoofing makes a call appear to come from a trusted source.'),
    ('vishing', 'If a caller pressures you to act immediately or face a penalty (like arrest or a fine), you should:', 'Act immediately to avoid the penalty.', 0, 'Be suspicious, as this is a high-pressure tactic used by scammers.', 1, 'Ask for their supervisor.', 0, 'Provide your social security number for verification.', 0, 'Correct! Legitimate organizations do not use threats or high-pressure tactics over the phone.'),
    ('vishing', 'A "tech support" vishing scam typically involves a scammer trying to:', 'Sell you a new computer.', 0, 'Gain remote access to your computer to "fix" a fake problem.', 1, 'Ask you survey questions.', 0, 'Schedule an in-person appointment.', 0, 'Correct! The goal is often to install malware or steal files once they have remote access.'),
    ('vishing', 'You get a voicemail saying you missed jury duty and a warrant is out for your arrest. To clear it, you must pay a fine with gift cards. This is:', 'A legitimate government request.', 0, 'A definite scam.', 1, 'A mistake you need to correct.', 0, 'A new payment method for fines.', 0, 'Correct! No government agency will ever demand payment in the form of gift cards.'),
    ('vishing', 'What is a key difference between vishing and phishing?', 'Vishing uses websites, while phishing uses email.', 0, 'Vishing is done over the phone, while phishing is primarily through email.', 1, 'Vishing targets companies, while phishing targets individuals.', 0, 'Vishing is legal, while phishing is not.', 0, 'Correct! The primary medium for vishing is voice (phone), while for phishing it is email.'),
    ('vishing', 'An effective way to handle a suspected vishing call is to:', 'Engage them in a long conversation to waste their time.', 0, 'Hang up without providing any information.', 1, 'Politely tell them you are not interested.', 0, 'Ask them to call you back later.', 0, 'Correct! The safest course of action is to simply hang up. Do not engage.'),
    ('vishing', 'Attackers can use AI voice-cloning technology to impersonate whom in a vishing call?', 'A celebrity', 0, 'A family member or your boss', 1, 'A historical figure', 0, 'A fictional character', 0, 'Correct! AI can be used to clone a known person\'s voice to make a vishing call highly convincing, often asking for emergency money transfers.'),

    # --- Category: Smishing (10 questions) ---
    ('smishing', 'What is "Smishing"?', 'Phishing via social media.', 0, 'Phishing via text message (SMS).', 1, 'Phishing via snail mail.', 0, 'A type of computer virus.', 0, 'Correct! Smishing is a phishing attack conducted using SMS (text messages).'),
    ('smishing', 'You receive a text: "FedEx: We have a package for you. Click here to schedule delivery: [suspicious link]". What should you do?', 'Click the link to get your package.', 0, 'Ignore and delete the text. If you are expecting a package, track it on the official FedEx website.', 1, 'Reply "STOP" to unsubscribe.', 0, 'Call the number back.', 0, 'Correct! Never trust links in unexpected delivery texts. Always use the official website or app.'),
    ('smishing', 'A common smishing tactic is to claim...', 'Your phone bill is lower than expected.', 0, 'A problem with a payment or account that requires immediate attention.', 1, 'A friend has sent you a photo.', 0, 'Your phone needs a software update.', 0, 'Correct! Like email phishing, smishing often creates a sense of urgency to trick you.'),
    ('smishing', 'Why can smishing be more effective than email phishing?', 'Text messages are longer than emails.', 0, 'People tend to trust text messages more and view them more quickly.', 1, 'Text messages can\'t be blocked.', 0, 'It\'s easier to see the full link on a phone.', 0, 'Correct! The personal and immediate nature of text messages can make people lower their guard.'),
    ('smishing', 'A text message from an unknown number says: "Hey, is this you in this picture? [link]". You should:', 'Click the link to see the picture.', 0, 'Delete the message immediately.', 1, 'Reply and ask who they are.', 0, 'Ask a friend if they sent it.', 0, 'Correct! This is a classic baiting tactic to get you to click on a malicious link.'),
    ('smishing', 'You receive a text with a one-time login code for an account you did not try to access. This could mean:', 'Someone is trying to access your account.', 1, 'It\'s a system glitch.', 0, 'It\'s a marketing text.', 0, 'Your friend is playing a prank.', 0, 'Correct! You should immediately go to that account (not via the text) and change your password.'),
    ('smishing', 'Smishing texts often come from...', 'Your own phone number.', 0, 'Numbers that look like regular phone numbers or short-code numbers.', 1, 'Email addresses.', 0, 'Your phone\'s manufacturer.', 0, 'Correct! They can come from a variety of numbers, often spoofed to look legitimate or anonymous.'),
    ('smishing', 'A text claiming to be from your bank asks you to reply with your PIN to "verify your identity." Your bank would:', 'Never ask for your PIN or full password via text.', 1, 'Routinely ask for this for security checks.', 0, 'Only ask for this if you call them first.', 0, 'Ask for this once a year.', 0, 'Correct! Legitimate financial institutions will never ask for sensitive data like PINs or passwords in a text message.'),
    ('smishing', 'The term "Smishing" is a combination of which two words?', 'Smart and Phishing', 0, 'SMS and Phishing', 1, 'Smile and Phishing', 0, 'Small and Phishing', 0, 'Correct! It combines SMS (Short Message Service) and Phishing.'),
    ('smishing', 'Which is a major red flag in a text message?', 'Using emojis.', 0, 'A link that uses a URL shortener (like bit.ly).', 1, 'A message from a known contact.', 0, 'Asking you to call a toll-free number.', 0, 'Correct! While not always malicious, URL shorteners hide the true destination of a link and are frequently used in smishing.'),

    # --- Category: Password Hygiene (10 questions) ---
    ('password-hygiene', 'What is the main problem with password reuse?', 'It\'s hard to remember which password you used.', 0, 'If one site is breached, attackers can access all your accounts using that password.', 1, 'It violates most websites\' terms of service.', 0, 'It slows down your login speed.', 0, 'Correct! This is called credential stuffing, and it\'s a very common attack vector.'),
    ('password-hygiene', 'Two-Factor Authentication (2FA) adds a second layer of security. What is an example of 2FA?', 'Using a password and a security question.', 0, 'A password and a code from a mobile app like Google Authenticator.', 1, 'Using two different passwords.', 0, 'A password and a PIN.', 0, 'Correct! 2FA combines something you know (password) with something you have (your phone).'),
    ('password-hygiene', 'How often should you ideally change your main passwords?', 'Every day.', 0, 'Only when a site tells you to.', 0, 'When you suspect an account has been compromised.', 1, 'Every year on your birthday.', 0, 'Correct! Modern advice is to use a unique, strong password and only change it if you suspect a breach, rather than on a fixed schedule.'),
    ('password-hygiene', 'What is the best way to store your unique passwords?', 'In a text file on your desktop named "passwords.txt".', 0, 'In your browser\'s password manager.', 0, 'In a dedicated, encrypted password manager application.', 1, 'Memorize all of them.', 0, 'Correct! A dedicated password manager is the most secure and convenient method.'),
    ('password-hygiene', 'What is a "passphrase"?', 'A very short password.', 0, 'A password that is a sequence of random words, making it long and memorable.', 1, 'A password that only works on one computer.', 0, 'The answer to a security question.', 0, 'Correct! For example, "Correct-Horse-Battery-Staple" is a famous example of a strong passphrase.'),
    ('password-hygiene', 'If a website offers 2FA, you should...', 'Ignore it because it\'s inconvenient.', 0, 'Enable it immediately.', 1, 'Only enable it for your most important accounts.', 0, 'Wait until it becomes mandatory.', 0, 'Correct! You should always enable 2FA wherever it is offered, especially for critical accounts like email and banking.'),
    ('password-hygiene', 'Which of the following is poor password hygiene?', 'Using a password manager.', 0, 'Enabling 2FA.', 0, 'Sharing your password with a trusted friend or family member.', 1, 'Using a long passphrase.', 0, 'Correct! You should never share your passwords with anyone, for any reason.'),
    ('password-hygiene', 'What is a potential risk of using public Wi-Fi to log into sensitive accounts?', 'It is slower than your home Wi-Fi.', 0, 'Attackers on the same network can potentially intercept your data.', 1, 'It uses more of your phone\'s battery.', 0, 'Most public Wi-Fi blocks secure websites.', 0, 'Correct! Unsecured networks are risky. It is best to use a VPN or your cellular data for sensitive logins.'),
    ('password-hygiene', 'Logging out of your accounts when you are finished using them, especially on public computers, is...', 'Unnecessary, as the browser will do it for you.', 0, 'A crucial security habit.', 1, 'Only important for social media.', 0, 'A waste of time.', 0, 'Correct! This prevents others who use the computer after you from accessing your accounts.'),
    ('password-hygiene', 'A site forces you to reset your password. After resetting it, you should...', 'Feel secure because you have a new password.', 0, 'Check for any suspicious activity on your account, like changed settings or emails.', 1, 'Immediately change it back to your old password.', 0, 'Delete your account.', 0, 'Correct! A forced reset could mean a company-wide breach. You should check your account for any unauthorized changes.'),

    # --- Category: Strong Passwords (strong-password) (10 questions) ---
    ('strong-password', 'Which of the following is the strongest password?', 'Password123!', 0, 'MyDogSparky', 0, 'e7G!k@Lp$z9#R2b', 1, '11111111', 0, 'Correct! It is long and contains a mix of uppercase letters, lowercase letters, numbers, and symbols.'),
    ('strong-password', 'What are the three core components of a strong password?', 'Length, humor, and obscurity.', 0, 'Length, complexity, and uniqueness.', 1, 'Your name, birthday, and pet\'s name.', 0, 'A common word, a number, and a symbol.', 0, 'Correct! A strong password must be long, complex (using different character types), and unique to that single account.'),
    ('strong-password', 'Why is "P@$$w0rd" a weak password?', 'It is too long.', 0, 'It uses common substitutions that hacking tools can easily guess.', 1, 'It does not contain your name.', 0, 'It is hard to type.', 0, 'Correct! Hackers\' dictionaries include common substitutions (like @ for a, 0 for o), making this password very easy to crack.'),
    ('strong-password', 'What is the most important factor for password strength?', 'The number of symbols used.', 0, 'The password\'s length.', 1, 'How often you change it.', 0, 'Whether it is a real word.', 0, 'Correct! A longer password is exponentially harder to crack than a short, complex one.'),
    ('strong-password', 'Using personal information like your birthdate or address in a password is a bad idea because...', 'It is hard for you to remember.', 0, 'This information can often be found publicly online.', 1, 'It is not complex enough.', 0, 'Most websites block personal information.', 0, 'Correct! Attackers can easily find this information and use it to guess your passwords.'),
    ('strong-password', 'A "brute-force attack" is when a hacker...', 'Tries to trick you into revealing your password.', 0, 'Uses software to try every possible combination of characters until the password is guessed.', 1, 'Steals your password from a company database.', 0, 'Looks over your shoulder.', 0, 'Correct! This is why password length is so critical; it makes brute-force attacks take much longer.'),
    ('strong-password', 'Which passphrase is the strongest?', 'i love my dog', 0, 'ILoveMyDog1!', 0, 'Blue-Giraffe-Eats-Quiet-Lamps', 1, 'password-password-password-password', 0, 'Correct! It is long, unpredictable, and easy to remember, which are the hallmarks of a good passphrase.'),
    ('strong-password', 'Is "12345678" a strong password?', 'Yes, because it is 8 characters long.', 0, 'No, because it is a very common and predictable sequence.', 1, 'Only if you add a symbol to it.', 0, 'Yes, if you use it for an unimportant site.', 0, 'Correct! It is one of the most common passwords in the world and would be cracked instantly.'),
    ('strong-password', 'The best way to create a strong, unique password for a new site is to:', 'Modify your existing main password slightly (e.g., adding "FB" at the end for Facebook).', 0, 'Use a trusted password manager to generate and save a random one for you.', 1, 'Think of a new clever phrase on the spot.', 0, 'Use the password suggested by the site.', 0, 'Correct! Password managers are excellent at creating and storing highly complex, random passwords.'),
    ('strong-password', 'Including a mix of uppercase letters, lowercase letters, numbers, and symbols in your password increases its:', 'Length', 0, 'Complexity', 1, 'Memorability', 0, 'Uniqueness', 0, 'Correct! This increases the total number of possible characters for each position, making it much harder to guess.'),

    # --- Category: Ransomware (10 questions) ---
    ('ransomware', 'How is ransomware typically delivered to a victim\'s computer?', 'Through a hardware device.', 0, 'Through phishing emails, malicious attachments, or compromised websites.', 1, 'Via phone calls.', 0, 'Through the mail.', 0, 'Correct! These are the most common infection vectors for ransomware.'),
    ('ransomware', 'What is the best defense against losing your files to ransomware?', 'Paying the ransom quickly.', 0, 'Having a recent, offline backup of your important files.', 1, 'A very strong password.', 0, 'Disconnecting from the internet after infection.', 0, 'Correct! If you have a backup, you can restore your files without needing to pay the attackers.'),
    ('ransomware', 'If your computer is infected with ransomware, should you pay the ransom?', 'Yes, it\'s the only way to get your files back.', 0, 'No, there is no guarantee you will get your files back, and it encourages the attackers.', 1, 'Only if the amount is small.', 0, 'Yes, but negotiate for a lower price.', 0, 'Correct! Security experts and law enforcement advise against paying, as it funds criminal activity and offers no guarantee of file recovery.'),
    ('ransomware', 'A common sign of a ransomware infection is:', 'Your computer running faster than usual.', 0, 'A pop-up message on your screen demanding payment.', 1, 'Receiving more spam email.', 0, 'Your webcam turning on by itself.', 0, 'Correct! The attackers will make it very clear that your files are encrypted and how to pay them.'),
    ('ransomware', 'Keeping your operating system and software up-to-date helps protect against ransomware because...', 'Updates make your files smaller.', 0, 'Updates often patch security vulnerabilities that ransomware exploits.', 1, 'Updates scan for existing viruses.', 0, 'Updates increase your internet speed.', 0, 'Correct! Many ransomware variants exploit known security flaws that have already been fixed in newer software versions.'),
    ('ransomware', 'Besides encrypting files, what other threat do modern ransomware gangs often use?', 'Deleting your web browser.', 0, 'Threatening to publicly leak the stolen data if the ransom isn\'t paid.', 1, 'Changing your desktop background.', 0, 'Overloading your printer.', 0, 'Correct! This is called double extortion and adds more pressure on victims to pay.'),
    ('ransomware', 'What is "crypto-locking"?', 'The process of buying cryptocurrency.', 0, 'The act of securing your files with a password.', 0, 'The process ransomware uses to encrypt your files, making them unreadable without a key.', 1, 'A type of digital currency.', 0, 'Correct! The ransomware encrypts the files and holds the decryption key hostage.'),
    ('ransomware', 'Can ransomware infect network drives and cloud-synced folders?', 'No, it only affects the local computer.', 0, 'Yes, it can spread to any connected drive or service.', 1, 'Only if they are on the same Wi-Fi network.', 0, 'Only on corporate networks.', 0, 'Correct! Any drive or folder your computer has write-access to is vulnerable, including shared network drives.'),
    ('ransomware', 'Using a reputable antivirus and anti-malware program can...', 'Make your computer immune to ransomware.', 0, 'Help detect and block many known ransomware variants before they can execute.', 1, 'Negotiate ransoms for you.', 0, 'Back up your files automatically.', 0, 'Correct! It provides a critical layer of defense, though it is not foolproof.'),
    ('ransomware', 'A hospital is forced to cancel appointments and divert ambulances. This is a real-world consequence of a...?', 'Phishing attack', 0, 'Ransomware attack', 1, 'Spyware infection', 0, 'Denial-of-service attack', 0, 'Correct! Ransomware attacks on critical infrastructure like hospitals have severe and dangerous real-world consequences.'),

    # --- Category: Spyware (10 questions) ---
    ('spyware', 'What is the main purpose of spyware?', 'To encrypt your files for a ransom.', 0, 'To secretly gather information about a person or organization and send it to another entity.', 1, 'To display unwanted advertisements.', 0, 'To replicate itself across a network.', 0, 'Correct! As the name implies, spyware is designed to spy on your activities.'),
    ('spyware', 'A program that secretly records every key you press is called a:', 'Keystroke recorder or keylogger.', 1, 'Trojan horse.', 0, 'Worm.', 0, 'Adware.', 0, 'Correct! Keyloggers are a dangerous form of spyware used to steal passwords and other sensitive information.'),
    ('spyware', 'How does spyware most commonly get onto a computer?', 'It is pre-installed on all new computers.', 0, 'Bundled with legitimate-looking "free" software downloads.', 1, 'Through a secured Wi-Fi network.', 0, 'By visiting the website of a major news organization.', 0, 'Correct! It often hides inside the installers of free programs, toolbars, or games.'),
    ('spyware', 'Which of the following is a common symptom of a spyware infection?', 'Your battery life suddenly improves.', 0, 'A sudden increase in pop-up ads or your browser homepage changing unexpectedly.', 1, 'Your files are all renamed with a strange extension.', 0, 'You receive fewer emails.', 0, 'Correct! These are signs that adware or browser-hijacking spyware is present.'),
    ('spyware', 'What is the difference between spyware and a computer virus?', 'There is no difference.', 0, 'A virus tries to replicate and spread, while spyware\'s main goal is to secretly collect data.', 1, 'Spyware is legal, but viruses are not.', 0, 'Viruses are for PCs, spyware is for Macs.', 0, 'Correct! While both are malware, their primary functions are different. A virus wants to spread; spyware wants to watch.'),
    ('spyware', 'Adware is a type of spyware that...', 'Steals your banking information.', 0, 'Tracks your browsing habits to display targeted advertisements.', 1, 'Records your webcam without permission.', 0, 'Encrypts your address book.', 0, 'Correct! Adware focuses on tracking you for advertising purposes, but can be a privacy risk.'),
    ('spyware', 'Can spyware be installed on mobile phones?', 'No, it only affects desktop computers.', 0, 'Yes, malicious apps can contain spyware.', 1, 'Only on Android phones.', 0, 'Only on iPhones.', 0, 'Correct! Spyware on phones can track location, read messages, and listen to calls.'),
    ('spyware', 'To protect yourself from spyware, you should:', 'Only download software from official and reputable sources.', 1, 'Click "agree" on all terms and conditions without reading.', 0, 'Disable your computer\'s firewall.', 0, 'Use the same password for everything.', 0, 'Correct! Avoid third-party download sites, which often bundle unwanted software.'),
    ('spyware', 'A program that appears to be a useful utility but secretly contains spyware is an example of a:', 'Worm', 0, 'Ransomware', 0, 'Trojan Horse', 1, 'Botnet', 0, 'Correct! A Trojan horse disguises malicious code within a seemingly legitimate program.'),
    ('spyware', 'The best tool for finding and removing existing spyware is:', 'Your computer\'s task manager.', 0, 'A reputable anti-spyware or anti-malware scanner.', 1, 'Your internet browser\'s history cleaner.', 0, 'Manually deleting suspicious files.', 0, 'Correct! These specialized tools are designed to detect and eliminate spyware that might be missed by traditional antivirus.')
]


# =========================================================================
#                             DATABASE SETUP
# =========================================================================
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# --- Create Tables ---
# Users Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL, last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE, password TEXT NOT NULL,
    reset_token TEXT, reset_token_expiration DATETIME
);
''')

# Questions Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL, question TEXT NOT NULL,
    answer1 TEXT NOT NULL, correct1 INTEGER NOT NULL,
    answer2 TEXT NOT NULL, correct2 INTEGER NOT NULL,
    answer3 TEXT NOT NULL, correct3 INTEGER NOT NULL,
    answer4 TEXT NOT NULL, correct4 INTEGER NOT NULL,
    feedback TEXT NOT NULL
);
''')

# User Progress Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL, category TEXT NOT NULL,
    high_score INTEGER NOT NULL, last_played_on DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
''')


# --- Populate the Questions Table ---
cursor.execute("SELECT COUNT(*) FROM questions")
if cursor.fetchone()[0] == 0:
    print("Questions table is empty. Inserting sample questions...")
    cursor.executemany("""
        INSERT INTO questions (category, question, answer1, correct1, answer2, correct2, answer3, correct3, answer4, correct4, feedback) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, sample_questions)
    print(f"{len(sample_questions)} sample questions have been added.")
else:
    print("Questions table already contains data. No new questions were added.")

# Commit changes and close
conn.commit()
conn.close()

print("\nDatabase initialization complete.")