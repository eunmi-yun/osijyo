from django import forms
from log.models import history

class StatusForm(forms.ModelForm):

    class Meta:
        model = history  # 사용할 모델
        fields = ['history_id']
        
        def __init__(self, *args, **kwargs):
            super(StatusForm, self).__init__(*args, **kwargs)
            historys = history.objects.all()
            status_codes = [(i.history_id) for i in historys]
            self.fields['status_code'] = forms.ChoiceField(choices=status_codes)