import { Component } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms'
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { CommonModule } from '@angular/common';
import { Login } from '../../../interface/auth.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Router, RouterModule } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';

@Component({
  selector: 'app-login',
  standalone:true,
  imports:[FormsModule, FontAwesomeModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent{
  icon = { faCircleXmark, faCircleCheck }
  userData:any;

  constructor(private _apiCall:ApiCallingService, private _router:Router, private _tostr:Toastr){}

  login(logForm:NgForm){
    // Creating data for comparison.
    let loginData:Login = {
      username: logForm.value.username!,
      password: logForm.value.password!
    }

    // Call api for authorisation.
    this._apiCall.postApi('auth/login/', loginData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {        
        // On success.
        if(response.status === false){
            this._tostr.toasterStatus(['text-[var(--dark-pink)]', response.msg]);
            this._router.navigate(['/auth']);
            return;
          }
          this._tostr.toasterStatus(['text-gray-600', response.msg]);
          this.userData = response.data
          this._router.navigate(['/']);
          return;
        }
    });
  }
}
