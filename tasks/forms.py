from django import forms
from tasks.models import Task

#Django Form
class TaskForm (forms.Form):
    title = forms.CharField(max_length=250, label='Task Title')
    description = forms.CharField(
        widget=forms.Textarea, label='Task Description')
    due_date = forms.DateField(widget=forms.SelectDateWidget, label="Due Date")
    assigned_to = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, choices =[], label="Assigned To")
    
    def __init__(self, *args, **kwargs):
        # print(args,kwargs)
        employees = kwargs.pop("employees", [])
        # print(employees)
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [
            (emp.id, emp.name) for emp in employees]
        
class SytledFormMixin:
      """Mixing to apply sytle to form field"""
      default_classes = "border-2 border-gray-400 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-600"
      
      def apply_styled_widgets(self):
          for field_name, field in self.fields.items():
              if isinstance(field.widget, forms.TextInput):
                  field.widget.attrs.update({
                      'class': self.default_classes,
                      'placeholder': f"Enter {field.label.lower()}",
                    })
              elif isinstance(field.widget, forms.Textarea):
                  field.widget.attrs.update({
                      'class': f"{self.default_classes}",
                      'style': 'resize: none;',
                      'placeholder': f"Enter {field.label.lower()}",
                      'rows':5
                   })
              elif isinstance(field.widget, forms.SelectDateWidget):
                  print("Inside Date")
                  field.widget.attrs.update({
                      'class':"border-2 border-gray-400 p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-600"
                  })
              elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                  print("Inside Checkbox")
                  field.widget.attrs.update({
                      'class': "space-y-2"
                  }) 
              else:
                  print("Inside else")
                  field.widget.attrs.update({
                      'class': self.default_classes
                  })
                
                
                  
# Django Model Form
class TaskModelForm(SytledFormMixin, forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.SelectDateWidget,
            'assigned_to': forms.CheckboxSelectMultiple
        }
      # exclude = ['project', 'is_completed', 'created_at', 'updated_at']
      
        '''Manual Widget'''
        # widgets = {
        #     'title': forms.TextInput(attrs={
        #         'class': "border-2 border-gray-400 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-600",
        #         'placeholder': "Enter a descriptive task title" 
        #     }),
        #     'description': forms.Textarea(attrs={
        #         'class': "border-2 border-gray-400 w-full p-3 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-600",
        #         'placeholder': "Provide detailed task information",
        #         'rows':5, #Added to define a consitent textarea hight
        #     }),
        #     'due_date': forms.SelectDateWidget(attrs={
        #         'class': "border-2 border-gray-400 p-2 rounded-lg shadow-sm focus:border-rose-500 focus:ring-rose-600",
        #     }),
        #     'assigned_to': forms.CheckboxSelectMultiple(attrs={
        #         'class': "space-y-2", #Added spacing betweend checkboxes for better readability
        #     })
        # }
    '''Widget Using Mixing Form'''  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()