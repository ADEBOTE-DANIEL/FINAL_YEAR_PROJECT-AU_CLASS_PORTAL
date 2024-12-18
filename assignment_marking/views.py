

from django.shortcuts import render
from .utils import extract_text_from_pdf, compare_assignments
from django.core.files.storage import FileSystemStorage

def mark_assignment(request):
    if request.method == 'POST' and request.FILES:
        teacher_pdf = request.FILES['teacher_pdf']  # Teacher reference PDF
        student_pdf = request.FILES['student_pdf']  # Student submission PDF

        # Optional file type validation
        if not (teacher_pdf.name.endswith('.pdf') and student_pdf.name.endswith('.pdf')):
            return render(request, 'assignment_marking/mark_assignment.html', {'error': 'Please upload PDF files only.'})

        # Extract text from PDFs
        teacher_text = extract_text_from_pdf(teacher_pdf)
        student_text = extract_text_from_pdf(student_pdf)

        # Debug: Ensure the text extraction is working
        print("Teacher Text:", teacher_text)
        print("Student Text:", student_text)

        # Call API to compare student submission with teacher reference
        comparison_result = compare_assignments(student_text, teacher_text)

        # Debug: Ensure comparison result is generated
        print("Comparison Result:", comparison_result)

        # Display the result
        return render(request, 'assignment_marking/result.html', {'result': comparison_result})

    return render(request, 'assignment_marking/mark_assignment.html')
