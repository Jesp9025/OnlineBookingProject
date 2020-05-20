# OnlineBookingProject
Online booking system based on Flask, SQLite and Python

<h2>Features:</h2>
<p>- Create/Register new account</p>
<p>- Login page with session</p>
<p>- Hashed passwords</p>
<p>- Navigation panel on top of website</p>
<p>- Bookings older than 1 day will be deleted and reserved resource quantity will be put back</p>
<p>- On booking, an email will be sent to the users registered email address</p>
<p>- Unique ID generator for user and booking creation</p>
<p>- View Resources & Bookings</p>
<p>- Make reservation/booking on equipment. Simply input ID of resource and quantity. It will be reserved for 24 hours.</p>
<p>- Delete bookings (admins can delete everything, users can only delete own bookings)</p>
<p>- Delete Resources(admins only)</p>
<p>- Update User: Username, password, email, admin status, delete user(admins only)</p>

<h2>Limitations:</h2>
<p>Not possible to book "into the future"</p>
<p>Meaning, when you create a booking, items/equipment is booked instantly for 1 day</p>

<h2>How to run:</h2>
<p>- run routes.py</p>
