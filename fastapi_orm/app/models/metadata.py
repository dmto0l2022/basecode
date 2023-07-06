from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

'''
`dropdown_valuepairs` (
  `variable` text DEFAULT NULL,
  `label` text DEFAULT NULL,
  `value` text DEFAULT NULL,
  `data_type` text DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
'''


class dropdown_valuepairs(models.Model):
    """
    The dropdown_valuepairs model
    """
    id = fields.IntField(pk=True)
    variable = fields.CharField(max_length=255, unique=True)
    label = fields.CharField(max_length=255, unique=True)
    value = fields.CharField(max_length=255, unique=True)
    data_type = fields.CharField(max_length=255, unique=True)
    
    
    class Meta:
        table="dropdown_valuepairs"
        ##schema = ""

dropdown_valuepair_Pydantic = pydantic_model_creator(Experiments, name="dropdown_valuepair")
dropdown_valuepairIn_Pydantic = pydantic_model_creator(Experiments, name="dropdown_valuepairIn", exclude_readonly=True)
