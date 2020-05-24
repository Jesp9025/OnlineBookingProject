<h1>OnlineBookingProject</h1>
<p>Online booking system based on HTML, Flask, SQLite and Python</p>
<p>Made by Jacob, Julius & Jesper at EADania Viborg</p>

<h2>Features:</h2>
<p>- Create/Register new account. Has 30 seconds cooldown</p>
<p>- Login page with session</p>
<p>- Hashed passwords</p>
<p>- Navigation panel on top of website</p>
<p>- Bookings older than 1 day will be deleted and reserved resource quantity will be put back</p>
<p>- On booking, user can choose to receive an email confirmation</p>
<p>- Unique ID generator for user,booking and resource creation</p>
<p>- View Resources & Bookings and search for specific</p>
<p>- Make reservation/booking on equipment. Simply input ID of resource and quantity. It will be reserved for 24 hours. Has 30 seconds cooldown</p>
<p>- Delete bookings (admins can delete everything, users can only delete own bookings)</p>
<p>- Create Resource</p>
<p>- Delete Resources(admins only)</p>
<p>- Update User: Username, password, email, admin status, delete user(admins only)</p>
<p>- Admin Logs. Logs will display if an admin made a change to a user and a list of all bookings made in history</p>
<p>- Bug submit. Email will be sent to an administrator</p>
<h2>Class Diagram</h2>
![Class Diagram]<img src="..\Class diagram - Booking system.png">
<h2>Limitations:</h2>
<p>Not possible to book "into the future"</p>
<p>Meaning, when you create a booking, items/equipment is booked instantly for 1 day</p>

<h2>How to run locally:</h2>
<p>- Run routes.py</p>
