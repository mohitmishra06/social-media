import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, FormsModule, NgForm, Validators } from '@angular/forms'
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { CommonModule } from '@angular/common';
import { Login } from '../../../interface/auth.interface';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-change-password',
  imports:[FormsModule, FontAwesomeModule, CommonModule],
  templateUrl: './change-password.html',
  styleUrls: ['./change-password.css']
})
export class ChangePasswordComponent implements OnInit {
  icon = { faCircleXmark, faCircleCheck }
  email:string = '';
  username:string = '';
  errorMessage:any;

  constructor(private _apiCall:ApiCallingService, private _router:Router, private _route: ActivatedRoute){}

  // Get params
  ngOnInit() {
    this._route.paramMap.subscribe(params => {
      this.email = params.get('id')!;
    });

    // Call api for authorisation.
    this._apiCall.getApiById('auth/user-details/', {"email":this.email}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        if(response.status === true){
          this.username = response.data;
          return;
        }
      }
    });
  }

  // Check user name
  checkUsername(event:any){
    console.log(event.target.value);
    
    // Call api for authorisation.
    this._apiCall.getApiById('auth/check-username/', {"username":event.target.value}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        if(response.status === true){
          console.log(response.msg);
          
          this.errorMessage = response.msg;
          console.log(this.errorMessage.msg);
          
          return;
        }
      }
    });    
  }

  changePassword(changeForm:NgForm){
    // Creating data for comparison.
    let changeData:Login = {
      username: changeForm.value.username!,
      password: changeForm.value.password!
    }

    // Call api for authorisation.
    this._apiCall.postApi('auth/change-password/', changeData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        this._router.navigate(['/auth']);
        return;
      }
    });
  }
}
