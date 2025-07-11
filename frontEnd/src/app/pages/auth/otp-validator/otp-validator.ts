import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, FormsModule, NgForm, Validators } from '@angular/forms'
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { CommonModule } from '@angular/common';
import { Login, OTP } from '../../../interface/auth.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';

@Component({
  selector: 'app-otp-validator',
  standalone:true,
  imports: [FormsModule, FontAwesomeModule, CommonModule],
  templateUrl: './otp-validator.html',
  styleUrl: './otp-validator.css'
})
export class OtpValidatorComponent implements OnInit{
  icon = { faCircleXmark, faCircleCheck }
  // Get otp in a string
  otp:string = ''
  email:string = '';

  constructor(
    private _apiCall:ApiCallingService,
    private _router:Router,
    private _route: ActivatedRoute,
    private _tostr:Toastr
  ){}

  // Get params
  ngOnInit() {
    this._route.paramMap.subscribe(params => {
      this.email = params.get('email')!;
    });    
  }

  // This function moves the focus after fill the input with number
  onInput(event: Event, nextInput: HTMLInputElement | null): void {
    const input = event.target as HTMLInputElement;
    if (input.value.length === 1 && nextInput) {
      nextInput.focus();
    }
  }

  // If we want to delete value from the input fields the focus moves backward again
  onBackspace(event: KeyboardEvent, prevInput: HTMLInputElement | null): void {
    const input = event.target as HTMLInputElement;
    if (event.key === 'Backspace' && input.value === '' && prevInput) {
      prevInput.focus();
    }
  }

  otpValidator(otpValidatorForm:NgForm){
    // Get all value in a value variable
    const formValue = otpValidatorForm.value;

    // Fill value in otp variable
    this.otp = formValue.first + formValue.second + formValue.third + formValue.fourth + formValue.fifth + formValue.six
    
    // Creating data for comparison.
    let otpData:OTP = {
      otp: this.otp,
      email:this.email
    }

    // Call api for otp verification.
    this._apiCall.getApi('auth/otp-validate/', otpData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr.toasterStatus(['text-[var(--dark-pink)]', response.msg]);
            return;
          }
          this._tostr.toasterStatus(['text-gray-600', response.msg]);
          this._router.navigate(['/auth/change-password/' + this.email]);
          return;
        }
    });

  }

  // Get new otp
  newOTP(){
    // Call api for new otp.
    this._apiCall.getApiById('auth/new-otp/', {'email':this.email}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success
        if(response.status === false){
          this._tostr.toasterStatus(['text-[var(--btn-danger)]', response.msg]);
          return;
        }        
        this._tostr.toasterStatus(['text-gray-600', response.msg]);
        return;
      }
    });
  }
}
