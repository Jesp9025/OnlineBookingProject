def sendEmail(email):
    import smtplib, ssl, functools, operator
    
    # Convert to string and remove symbols :O
    toList = functools.reduce(operator.add, (email))
    actualEmail = toList.replace("(", "")
    actualEmail = actualEmail.replace("'", "")
    actualEmail = actualEmail.replace(")", "")
    actualEmail = actualEmail.replace(",", "")
    print(actualEmail)
    
    port = 465  # For SSL
    password = 'asdjj34j34jasjdajasdlakkl!"#"asdasdki'

    #Content of email
    sender_email = "bookingprojectEaDania@gmail.com"
    receiver_email = actualEmail
    message = """\
    Subject: Hi there

    Your booking has been confirmed."""

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("bookingprojectEaDania@gmail.com", password)
        server.sendmail(sender_email, receiver_email, message)