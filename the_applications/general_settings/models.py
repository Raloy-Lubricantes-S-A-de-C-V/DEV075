from django.db import models
class ModelConfig(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.title


class ModelBackground(models.Model):
    pk_config = models.ForeignKey(ModelConfig,on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    img = models.ImageField(upload_to='background')
    alt = models.CharField(max_length=100)

    def __str__(self):
        return self.alt