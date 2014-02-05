from bs4 import BeautifulSoup
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib2 import urlopen


newhtml = urlopen("https://secure.nationaltheatre.org.uk/performanceCalendar?iframe=1&returnUrl=shows%252Fblurred-lines%253Fdates%253Dall&prodno=44001&syos=&ba_only=&ba_only=1&year=all&month=all&hide=&mos=0").read()

oldhtml = ""
with open('/home/james/downloaded.html', 'rb') as fp:
	oldhtml = fp.read()

soupnew = BeautifulSoup(newhtml)
soupold = BeautifulSoup(oldhtml)

if soupnew.find_all("li") != soupold.find_all("li"):
	print "Tickets - found a change"
	dates = '<p><a href="http://www.nationaltheatre.org.uk/shows/blurred-lines?dates=all#tabpos">Show URL</a> </p>'
	dates = dates + "<p>Available dates: </p><ul>"

	for li in soupnew.find_all("li"):
		if li.find("a"):
			dates = dates + li.__str__()

	dates = dates + "</ul>"
	dates = dates + "<p>All dates:</p><ul>"

	for li in soupnew.find_all("li"):
		dates = dates + li.__str__()
	dates = dates + "</ul>"
	dates = dates.replace('href="/', 'href="http://secure.nationaltheatre.org.uk/')
	message_body = "<p>The availability has changed:</p>" + dates
	html = MIMEText(message_body, 'html')
	message = MIMEMultipart()
	message.attach(html)
	message['Subject'] = "Change of Availability"
	message['From'] = ""
	message['To'] = ""
	smtp = SMTP("smtp.mailgun.org", 587)
	smtp.login("", "")
	smtp.sendmail("", "", message.as_string())
	smtp.quit()

with open('/home/james/downloaded.html', 'w') as fp:
	fp.write(newhtml)
