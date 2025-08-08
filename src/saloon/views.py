from django.shortcuts import render, redirect

# Create your views here.

def redirectHome():
    return redirect('home')

def home(): 
    ...