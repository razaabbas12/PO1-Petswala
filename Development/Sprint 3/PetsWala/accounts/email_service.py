import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_service_provider_approved_email(receiver_address):
  try:
    mail_content = """<!DOCTYPE html>
    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

    <head>
      <title></title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
      <!--[if !mso]><!-->
      <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Permanent+Marker" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Abril+Fatface" rel="stylesheet" type="text/css">
      <!--<![endif]-->
      <style>
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          padding: 0;
        }

        a[x-apple-data-detectors] {
          color: inherit !important;
          text-decoration: inherit !important;
        }

        #MessageViewBody a {
          color: inherit;
          text-decoration: none;
        }

        p {
          line-height: inherit
        }

        @media (max-width:700px) {
          .icons-inner {
            text-align: center;
          }

          .icons-inner td {
            margin: 0 auto;
          }

          .row-content {
            width: 100% !important;
          }

          .stack .column {
            width: 100%;
            display: block;
          }
        }
      </style>
    </head>

    <body style="background-color: #f9f9f9; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
      <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f9f9f9;">
        <tbody>
          <tr>
            <td>
              <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #cbdbef; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 20px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="image_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="width:100%;padding-right:0px;padding-left:0px;padding-top:70px;">
                                    <div align="center" style="line-height:10px"><img src="https://d1oco4z2z1fhwp.cloudfront.net/templates/default/4971/check-icon.png" style="display: block; height: auto; border: 0; width: 93px; max-width: 100%;" width="93" alt="Check Icon" title="Check Icon"></div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:25px;padding-left:20px;padding-right:20px;padding-top:10px;">
                                    <div style="font-family: Georgia, 'Times New Roman', serif">
                                      <div style="font-size: 14px; font-family: Georgia, Times, 'Times New Roman', serif; mso-line-height-alt: 16.8px; color: #2f2f2f; line-height: 1.2;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:42px;">Approved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:80px;padding-left:30px;padding-right:30px;padding-top:10px;">
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 21px; color: #2f2f2f; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">Hi,</span></p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;">&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center;">Your Service Provider Application has been approved.&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;"><span style="color:#000000;font-size:14px;">Sign In to Get Started.</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:30px;">
                                    <div style="font-family: Arial, sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 21px; color: #f9f9f9; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 36px;"><span style="font-size:24px;"><strong><span style>PetsWala</span></strong></span><span style="font-size:24px;"></span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">Visit now at https://petswala.site</span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">petswalasite@gmail.com </span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td>
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #cfceca; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:12px;">2022 © All Rights Reserved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="icons_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="color:#9d9d9d;font-family:inherit;font-size:15px;padding-bottom:5px;padding-top:5px;text-align:center;">
                                    <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                      <tr>
                                        <td style="text-align:center;">
                                          <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                          <!--[if !vml]><!-->
                                        </td>
                                      </tr>
                                    </table>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table><!-- End -->
    </body>

    </html>"""

    #The mail addresses and password
    sender_address = 'petswalasite@gmail.com'
    sender_pass = 'Petswala#1324'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Service Provider Account Approved'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return True
  except:
    return False


def send_rescue_service_approved_email(receiver_address):
  try:
    mail_content = """<!DOCTYPE html>
    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

    <head>
      <title></title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
      <!--[if !mso]><!-->
      <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Permanent+Marker" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Abril+Fatface" rel="stylesheet" type="text/css">
      <!--<![endif]-->
      <style>
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          padding: 0;
        }

        a[x-apple-data-detectors] {
          color: inherit !important;
          text-decoration: inherit !important;
        }

        #MessageViewBody a {
          color: inherit;
          text-decoration: none;
        }

        p {
          line-height: inherit
        }

        @media (max-width:700px) {
          .icons-inner {
            text-align: center;
          }

          .icons-inner td {
            margin: 0 auto;
          }

          .row-content {
            width: 100% !important;
          }

          .stack .column {
            width: 100%;
            display: block;
          }
        }
      </style>
    </head>

    <body style="background-color: #f9f9f9; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
      <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f9f9f9;">
        <tbody>
          <tr>
            <td>
              <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #cbdbef; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 20px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="image_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="width:100%;padding-right:0px;padding-left:0px;padding-top:70px;">
                                    <div align="center" style="line-height:10px"><img src="https://d1oco4z2z1fhwp.cloudfront.net/templates/default/4971/check-icon.png" style="display: block; height: auto; border: 0; width: 93px; max-width: 100%;" width="93" alt="Check Icon" title="Check Icon"></div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:25px;padding-left:20px;padding-right:20px;padding-top:10px;">
                                    <div style="font-family: Georgia, 'Times New Roman', serif">
                                      <div style="font-size: 14px; font-family: Georgia, Times, 'Times New Roman', serif; mso-line-height-alt: 16.8px; color: #2f2f2f; line-height: 1.2;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:42px;">Approved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:80px;padding-left:30px;padding-right:30px;padding-top:10px;">
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 21px; color: #2f2f2f; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">Hi,</span></p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;">&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center;">Your Rescue Service Application has been approved.&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;"><span style="color:#000000;font-size:14px;">Sign In to Get Started.</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:30px;">
                                    <div style="font-family: Arial, sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 21px; color: #f9f9f9; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 36px;"><span style="font-size:24px;"><strong><span style>PetsWala</span></strong></span><span style="font-size:24px;"></span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">Visit now at https://petswala.site</span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">petswalasite@gmail.com </span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td>
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #cfceca; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:12px;">2022 © All Rights Reserved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="icons_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="color:#9d9d9d;font-family:inherit;font-size:15px;padding-bottom:5px;padding-top:5px;text-align:center;">
                                    <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                      <tr>
                                        <td style="text-align:center;">
                                          <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                          <!--[if !vml]><!-->
                                        </td>
                                      </tr>
                                    </table>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table><!-- End -->
    </body>

    </html>"""

    #The mail addresses and password
    sender_address = 'petswalasite@gmail.com'
    sender_pass = 'Petswala#1324'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Rescue Service Account Approved'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return True
  except:
    return False
  

def send_vets_approved_email(receiver_address):
  try:
    mail_content = """<!DOCTYPE html>
    <html xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office" lang="en">

    <head>
      <title></title>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <!--[if mso]><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch><o:AllowPNG/></o:OfficeDocumentSettings></xml><![endif]-->
      <!--[if !mso]><!-->
      <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Lato" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Roboto" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Permanent+Marker" rel="stylesheet" type="text/css">
      <link href="https://fonts.googleapis.com/css?family=Abril+Fatface" rel="stylesheet" type="text/css">
      <!--<![endif]-->
      <style>
        * {
          box-sizing: border-box;
        }

        body {
          margin: 0;
          padding: 0;
        }

        a[x-apple-data-detectors] {
          color: inherit !important;
          text-decoration: inherit !important;
        }

        #MessageViewBody a {
          color: inherit;
          text-decoration: none;
        }

        p {
          line-height: inherit
        }

        @media (max-width:700px) {
          .icons-inner {
            text-align: center;
          }

          .icons-inner td {
            margin: 0 auto;
          }

          .row-content {
            width: 100% !important;
          }

          .stack .column {
            width: 100%;
            display: block;
          }
        }
      </style>
    </head>

    <body style="background-color: #f9f9f9; margin: 0; padding: 0; -webkit-text-size-adjust: none; text-size-adjust: none;">
      <table class="nl-container" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #f9f9f9;">
        <tbody>
          <tr>
            <td>
              <table class="row row-1" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #cbdbef; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 20px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="image_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="width:100%;padding-right:0px;padding-left:0px;padding-top:70px;">
                                    <div align="center" style="line-height:10px"><img src="https://d1oco4z2z1fhwp.cloudfront.net/templates/default/4971/check-icon.png" style="display: block; height: auto; border: 0; width: 93px; max-width: 100%;" width="93" alt="Check Icon" title="Check Icon"></div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:25px;padding-left:20px;padding-right:20px;padding-top:10px;">
                                    <div style="font-family: Georgia, 'Times New Roman', serif">
                                      <div style="font-size: 14px; font-family: Georgia, Times, 'Times New Roman', serif; mso-line-height-alt: 16.8px; color: #2f2f2f; line-height: 1.2;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:42px;">Approved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:80px;padding-left:30px;padding-right:30px;padding-top:10px;">
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, Helvetica Neue, Helvetica, sans-serif; mso-line-height-alt: 21px; color: #2f2f2f; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 24px;"><span style="font-size:16px;">Hi,</span></p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;">&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center;">Your Veterinary Doctor Application has been approved.&nbsp;</p>
                                        <p style="margin: 0; font-size: 14px; text-align: center; mso-line-height-alt: 21px;"><span style="color:#000000;font-size:14px;">Sign In to Get Started.</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-2" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td style="padding-bottom:10px;padding-left:10px;padding-right:10px;padding-top:30px;">
                                    <div style="font-family: Arial, sans-serif">
                                      <div style="font-size: 14px; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; mso-line-height-alt: 21px; color: #f9f9f9; line-height: 1.5;">
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 36px;"><span style="font-size:24px;"><strong><span style>PetsWala</span></strong></span><span style="font-size:24px;"></span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">Visit now at https://petswala.site</span></p>
                                        <p style="margin: 0; font-size: 12px; text-align: center; mso-line-height-alt: 18px;"><span style="font-size:12px;">petswalasite@gmail.com </span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-3" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; background-color: #5d77a9; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 0px; padding-bottom: 20px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="text_block" width="100%" border="0" cellpadding="10" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; word-break: break-word;">
                                <tr>
                                  <td>
                                    <div style="font-family: sans-serif">
                                      <div style="font-size: 12px; mso-line-height-alt: 14.399999999999999px; color: #cfceca; line-height: 1.2; font-family: Arial, Helvetica Neue, Helvetica, sans-serif;">
                                        <p style="margin: 0; font-size: 14px; text-align: center;"><span style="font-size:12px;">2022 © All Rights Reserved</span></p>
                                      </div>
                                    </div>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
              <table class="row row-4" align="center" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                <tbody>
                  <tr>
                    <td>
                      <table class="row-content stack" align="center" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; color: #000000; width: 680px;" width="680">
                        <tbody>
                          <tr>
                            <td class="column" width="100%" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt; font-weight: 400; text-align: left; vertical-align: top; padding-top: 5px; padding-bottom: 5px; border-top: 0px; border-right: 0px; border-bottom: 0px; border-left: 0px;">
                              <table class="icons_block" width="100%" border="0" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                <tr>
                                  <td style="color:#9d9d9d;font-family:inherit;font-size:15px;padding-bottom:5px;padding-top:5px;text-align:center;">
                                    <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="mso-table-lspace: 0pt; mso-table-rspace: 0pt;">
                                      <tr>
                                        <td style="text-align:center;">
                                          <!--[if vml]><table align="left" cellpadding="0" cellspacing="0" role="presentation" style="display:inline-block;padding-left:0px;padding-right:0px;mso-table-lspace: 0pt;mso-table-rspace: 0pt;"><![endif]-->
                                          <!--[if !vml]><!-->
                                        </td>
                                      </tr>
                                    </table>
                                  </td>
                                </tr>
                              </table>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </td>
                  </tr>
                </tbody>
              </table>
            </td>
          </tr>
        </tbody>
      </table><!-- End -->
    </body>

    </html>"""

    #The mail addresses and password
    sender_address = 'petswalasite@gmail.com'
    sender_pass = 'Petswala#1324'

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Veterinary Doctor Account Approved'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'html'))

    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    return True
  except:
    return False