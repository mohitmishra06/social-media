import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, FormsModule, NgForm, Validators } from '@angular/forms'
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { CommonModule } from '@angular/common';
import { Login } from '../../../interface/auth.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Router, RouterModule } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone:true,
  imports:[FormsModule, FontAwesomeModule, CommonModule, RouterModule],
  templateUrl: './login.html',
  styleUrls: ['./login.css']
})
export class LoginComponent {
  icon = { faCircleXmark, faCircleCheck }
  constructor(private _apiCall:ApiCallingService, private _router:Router){}

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
        if(response.success === false){
          this._router.navigate(['/auth']);
          return;
        }
        this._router.navigate(['/']);
        return;
      }
    });
  }

  // Logout
  logout(){
    // Call api for authorisation.
    this._apiCall.getApi('auth/logout/').subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
          this._router.navigate(['/auth']);
      }
    });
  }
}
