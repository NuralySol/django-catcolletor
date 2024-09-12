from django.db import models
from datetime import date

# A tuple of 2-tuples
MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    
    # new code below and you can create def's to see them print out in the python shell
    def __str__(self):
        return self.name
    # fed for today method must import date
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)
    
# Add new Feeding model below Cat model
class Feeding(models.Model):
    date = models.DateField('Feeding Date')
    meal = models.CharField(
    max_length=1,
    # add the 'choices' field option
    choices=MEALS,
    # set the default value for meal to be 'B'
    default=MEALS[0][0]
    )
    # Create a cat_id FK
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)
    
    def __str__(self):
    # Nice method for obtaining the friendly value of a Field.choice
        return f"{self.get_meal_display()} on {self.date}"
    
    # change the default sort Meta nested class
    class Meta:
        ordering = ['-date']
    
# Add the Toy model
class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.name

