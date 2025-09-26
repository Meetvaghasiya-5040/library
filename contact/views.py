

from django.contrib import messages
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import redirect, render

from Books.utils import check_internet

from .models import ContactUs


def about(request):
    internet = check_internet()
    return render(request, 'about.html', {'internet': internet})

def contact(request):
    internet = check_internet()
    
    if request.method == 'POST':
        try:
            
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            
            if not all([first_name, last_name, email, subject, message]):
                messages.error(request, 'Please fill in all required fields.')
                return render(request, 'contact.html', {'internet': internet})
            

            
            
            
            contact_instance = ContactUs.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
                # Send email notification
            email_subject = f'New Contact Form Submission: {subject}'
            email_message = (
                    f'Name: {first_name} {last_name}\n'
                    f'Email: {email}\n'
                    f'Phone: {phone}\n'
                    f'Subject: {subject}\n'
                    f'Message: \n Thank you for give your feedback !\n Our team will contact you soon for your peoblem : {message} . We will Solw your problem very soon !'
                )
            send_mail(
                    email_subject,
                    email_message,
                    None,
                    [email],
                    fail_silently=False,
                )
            
            messages.success(
                request, 
                f'Thank you {first_name}! Your message has been submitted successfully. '
                'We will get back to you within 24 hours.'
            )
            
            return redirect('contact')
            
        except IntegrityError:
            messages.error(request,'Yout Phone Number Is Already Registered !')

        except Exception as e:
            
            print(f"Contact form error: {e}")
            messages.error(
                request, 
                'An error occurred while submitting your message. Please try again.'
            )
        
    return render(request, 'contact.html', {'internet': internet})