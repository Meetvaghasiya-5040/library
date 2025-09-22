

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactUs
from Books.utils import check_internet

def about(request):
    internet = check_internet()
    return render(request, 'about.html', {'internet': internet})

def contact(request):
    internet = check_internet()
    
    if request.method == 'POST':
        try:
            
            first_name = request.POST.get('firstName', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            
            
            if not all([first_name, last_name, email, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'contact.html', {'internet': internet})
            

            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                messages.error(request, 'Please enter a valid email address.')
                return render(request, 'contact.html', {'internet': internet})
            
            
            contact_instance = ContactUs.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            
            messages.success(
                request, 
                f'Thank you {first_name}! Your message has been submitted successfully. '
                'We will get back to you within 24 hours.'
            )
            
            return redirect('contact')
            
        except Exception as e:
            
            print(f"Contact form error: {e}")
            messages.error(
                request, 
                'An error occurred while submitting your message. Please try again.'
            )
    
    return render(request, 'contact.html', {'internet': internet})