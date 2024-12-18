

from django import forms
from ckeditor.widgets import CKEditorWidget

# from classroom.models import Course, Category

class AssignmentUploadForm(forms.Form):
    teacher_pdf = forms.FileField(label='Teacher Reference PDF', required=True, widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))
    student_pdf = forms.FileField(label='Student Assignment PDF', required=True, widget=forms.ClearableFileInput(attrs={'accept': '.pdf'}))

    # Ensure both files are PDFs
    def clean_teacher_pdf(self):
        file = self.cleaned_data.get('teacher_pdf')
        if file and not file.name.endswith('.pdf'):
            raise forms.ValidationError('Teacher file must be a PDF.')
        return file

    def clean_student_pdf(self):
        file = self.cleaned_data.get('student_pdf')
        if file and not file.name.endswith('.pdf'):
            raise forms.ValidationError('Student file must be a PDF.')
        return file
