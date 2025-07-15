import { Component, Input, OnInit } from '@angular/core';
import { ChangePasswordDetails, UpdatePersonalDetails, User } from '../../../interface/user.interface';
import { CommonModule } from '@angular/common';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { environment } from '../../../../environments/environment.development';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCamera, faClose, faPen } from '@fortawesome/free-solid-svg-icons';
import { AbstractControl, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-update-user',
  imports: [CommonModule, FontAwesomeModule, ReactiveFormsModule],
  templateUrl: './update-user.html',
  styleUrl: './update-user.css'
})
export class UpdateUser implements OnInit{
  icon = { faClose, faPen, faCamera }
  @Input() currentuser?:User;
  isOpenModal:boolean = false     // This decide the modal will open or close
  isTabOpen:boolean = true;
  userDetails:any;
  url:string = environment.IMG_BASEURL;
  updateForm:any;
  changePasswordForm:any;

  constructor(
    private _apiCall:ApiCallingService,
    private _tostr:Toastr
  ){}

  ngOnInit(): void {
    // If user id comes getUserdetails function will call.
    if (this.currentuser) {
      this.getUserDetails(this.currentuser);
    } else {
      console.warn('User is undefined');
    }    
  }
  
  // only email and number are allow
  emailOrNumberAllow(frm: AbstractControl) {
    let emlRgx = /^[^\s@A-Z]+@[^\s@A-Z0-9]+\.[^\s@A-Z0-9]+$/;
    let numRgx = /^[0-9]*$/;
       
   return ((emlRgx.test(frm.get('email')?.value) ) || (numRgx.test(frm.get('email')?.value))) ?
     null: {mismatch:true}
  }

  // Modal open close
  setOpen(){
    this.isOpenModal = this.isOpenModal ? false : true;
  }

  // Tab open close
  setTabOpen(data:boolean){
    this.isTabOpen = data; 
  }

  // FUNCTION FOR UPDATION
  // Fetch current user details
  getUserDetails(id:User){
    this._apiCall.getApi("auth/user-details/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.userDetails = response.data;
          console.log(this.userDetails);
          // MAKE FORMS
          // Personal details
          this.updateForm = new FormGroup({
            name: new FormControl(this.userDetails.name, Validators.compose([Validators.required])),
            surname: new FormControl(this.userDetails.surname, Validators.compose([Validators.required])),
            email: new FormControl(this.userDetails.email, Validators.compose([Validators.required])),
            school: new FormControl(this.userDetails.school, Validators.compose([Validators.required])),
            work: new FormControl(this.userDetails.work, Validators.compose([Validators.required])),
            website: new FormControl(this.userDetails.website, Validators.compose([Validators.required])),
            city: new FormControl(this.userDetails.city, Validators.compose([Validators.required])),
            desc: new FormControl(this.userDetails.desc, Validators.compose([Validators.required]))
          }, {validators: this.emailOrNumberAllow});

          // Change password and Username
          this.changePasswordForm = new FormGroup({
            username: new FormControl(this.userDetails.username, Validators.compose([Validators.required])),
            password: new FormControl(this.userDetails.password, Validators.compose([Validators.required, Validators.minLength(8)]))
          }, {validators: this.emailOrNumberAllow});
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Personal details
  updateDetails(){
    let updateData:UpdatePersonalDetails = {
      name: this.updateForm.value.name!,
      surname: this.updateForm.value.surname!,
      email: this.updateForm.value.email!,
      school: this.updateForm.value.school!,
      work: this.updateForm.value.work!,
      website: this.updateForm.value.website!,
      city: this.updateForm.value.city!,
      desc: this.updateForm.value.desc!,
    }

    let data = {
      id:this.currentuser,
      personal:updateData
    }

    this._apiCall.getApi("auth/user-details/", data).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.userDetails = response.data;
          console.log(this.userDetails);
          
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }
  
  // Password and Username change
  changePassword(){
    let changePassword:ChangePasswordDetails = {
      username: this.changePasswordForm.value.username!,
      password: this.changePasswordForm.value.password!,
    }

    let data = {
      id:this.currentuser,
      credentials:changePassword
    }

    this._apiCall.getApi("auth/change-password/", data).subscribe({
      next: (response: any) => {
        if (response.status === true) {        
          this.userDetails = response.data;
          console.log(this.userDetails);
          
          // Maybe redirect or show an alert
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.error])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Banner images change
  updateBanner(event: Event){
    const file = (event.target as HTMLInputElement)?.files?.[0];
    if (file) {
      console.log('Profile image selected:', file);
    }
  }

  // Profile image
  updateUserImage(event: Event){
    const file = (event.target as HTMLInputElement)?.files?.[0];
    if (file) {
      console.log('Profile image selected:', file);
    }
  }
}
