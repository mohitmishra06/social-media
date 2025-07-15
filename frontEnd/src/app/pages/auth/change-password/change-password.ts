import { Component, OnInit } from '@angular/core';
import { FormsModule, NgForm } from '@angular/forms'
import { faCircleCheck, faCircleXmark } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome'
import { CommonModule } from '@angular/common';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Toastr } from '../../../services/toastr/toastr';
import { Change } from '../../../interface/auth.interface';

@Component({
  selector: 'app-change-password',
  imports:[FormsModule, FontAwesomeModule, CommonModule],
  templateUrl: './change-password.html',
  styleUrls: ['./change-password.css']
})
export class ChangePasswordComponent implements OnInit {
  icon = { faCircleXmark, faCircleCheck }
  userId:string = '';
  username:string = '';
  errorMessage:any;

  constructor(private _apiCall:ApiCallingService, private _router:Router, private _route: ActivatedRoute, private _tostr:Toastr){}

  // Get params
  ngOnInit() {
    this._route.paramMap.subscribe(params => {
      this.userId = params.get('id')!;
    });

    // Call api for user details.
    this._apiCall.getApiById('auth/user-details/', {"id":this.userId}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        if(response.status === true){
          this.username = response.data.username;
          return;
        }
      }
    });
  }

  // Check user name
  checkUsername(event:any){    
    // Call api for user exist or not.
    this._apiCall.getApiById('auth/check-username/', {"username":event.target.value}).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        if(response.status === true){
          this.errorMessage = response.msg;
          return;
        }
      }
    });    
  }

  changePassword(changeForm:NgForm){
    // Creating data for comparison.
    let changeData:Change = {
      id: this.userId,
      username: changeForm.value.username!,
      password: changeForm.value.password!
    }

    // Call api for authorisation.
    this._apiCall.putApi('auth/change-password/', changeData).subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr.toasterStatus(['text-red', response.msg]);
            return;
          }
          this._tostr.toasterStatus(['text-gray-600', response.msg]);
          this._router.navigate(['/auth']);
          return;
      }
    });
  }
}
