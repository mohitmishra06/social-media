import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Register } from '../../../interface/auth.interface';
import { Router } from '@angular/router';

@Component({
  selector: 'app-forgot-password',
  templateUrl: './forgot-password.html',
  styleUrls: ['./forgot-password.css'],
  imports: [ReactiveFormsModule, CommonModule, FontAwesomeModule]
})
export class ForgotPasswordComponent {

  icon = {faCircleXmark, faCircleCheck}
  constructor(private _apiCall:ApiCallingService, private _router:Router){}
  
  // only email and number are allow
  emailOrNumberAllow(frm: AbstractControl) {
    let emlRgx = /^[^\s@A-Z]+@[^\s@A-Z0-9]+\.[^\s@A-Z0-9]+$/;
    let numRgx = /^[0-9]*$/;
       
   return ((emlRgx.test(frm.get('email')?.value) ) || (numRgx.test(frm.get('email')?.value))) ?
     null: {mismatch:true}
  }
  
  fogForm = new FormGroup({
    email:new FormControl('', Validators.compose([Validators.required]))
  }, {validators: this.emailOrNumberAllow})

  forgotPassword(){
    console.log("this.regForm.value.email");

    // Creating data for comparison.
    let forgotData:Register = {
      email: this.fogForm.value.email!,
    }

    // Call api for authorisation.
    this._apiCall.postApi('auth/new-otp/', forgotData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.success === false){
          this._router.navigate(['/auth']);
          return;
        }
        
        this._router.navigate(['/auth/otp-validator']);
        return;
      }
    });
  }
}
