import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Register } from '../../../interface/auth.interface';
import { Router, RouterModule } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';

@Component({
  selector: 'app-register',
  standalone:true,
  imports:[ReactiveFormsModule, CommonModule, FontAwesomeModule, RouterModule],
  templateUrl: './register.html',
  styleUrls: ['./register.css']
})
export class RegisterComponent {

  icon = {faCircleXmark, faCircleCheck}
  constructor(private _apiCall:ApiCallingService, private _router:Router, private _tostr:Toastr){}
  
  // only email and number are allow
  emailOrNumberAllow(frm: AbstractControl) {
    let emlRgx = /^[^\s@A-Z]+@[^\s@A-Z0-9]+\.[^\s@A-Z0-9]+$/;
    let numRgx = /^[0-9]*$/;
       
   return ((emlRgx.test(frm.get('email')?.value) ) || (numRgx.test(frm.get('email')?.value))) ?
     null: {mismatch:true}
  }
  
  regForm = new FormGroup({
    email:new FormControl('', Validators.compose([Validators.required]))
  }, {validators: this.emailOrNumberAllow})

  register(){
    console.log("this.regForm.value.email");

    // Creating data for comparison.
    let registerData:Register = {
      email: this.regForm.value.email!,
    }

    // Call api for authorisation.
    this._apiCall.postApi('auth/register/', registerData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr.toasterStatus(['text-[var(--dark-pink)]', response.msg]);
            return;
          }
          this._tostr.toasterStatus(['text-gray-600', response.msg]);
          this._router.navigate(['/auth/otp-validator/'+response.data]);
          return;
      }
    });
  }
}
