from django.db import models
from common.models import User

yangi = 'yangi'
moderatsiya = 'moderatsiyada'
tasdiqlangan = 'tasdiqlangan'
STATUS = [
    (yangi, "yangi"),
    (moderatsiya, "moderatsiyada"),
    (tasdiqlangan, 'tasdiqlangan')

]
yuridik = 'yuridik'
jismoniy = 'jismoniy'

TYPE_OF_SPONSOR = [
    (yuridik, "yuridik"),
    (jismoniy, "jismoniy"),

]


class Sponsor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sponsors')
    name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    wallet = models.PositiveBigIntegerField()
    type_sponsor = models.CharField(choices=TYPE_OF_SPONSOR, max_length=15)
    status = models.CharField(max_length=25, choices=STATUS, default=yangi)
    organization_name = models.CharField(max_length=250, null=True, blank=True)
    datesp = models.DateTimeField()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
    full_name = models.CharField(max_length=250)
    phone = models.CharField(max_length=15)
    otm = models.CharField(max_length=250)
    type_student = models.CharField(max_length=100)
    contract_summ = models.PositiveBigIntegerField()
    wallet = models.PositiveBigIntegerField(default=0)
    datest = models.DateTimeField()

    def __str__(self):
        return self.full_name


class Contract(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contracts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='contracts')
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name='contracts')
    payment = models.PositiveBigIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
