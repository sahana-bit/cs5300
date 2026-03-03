from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title


class Seat(models.Model):
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return self.seat_number


class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="showtimes")
    start_time = models.DateTimeField()

    class Meta:
        ordering = ["start_time"]

    def __str__(self):
        return f"{self.movie.title} @ {self.start_time}"


class Booking(models.Model):
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, related_name="bookings")
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["showtime", "seat"], name="unique_seat_per_showtime")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.showtime} - {self.seat.seat_number}"