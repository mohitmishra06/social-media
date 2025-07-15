import { Component, Input, OnInit } from '@angular/core';
import { ChangePasswordDetails, UpdatePersonalDetails, User } from '../../../interface/user.interface';
import { CommonModule } from '@angular/common';
import { ApiCallingService } from '../../../services/api/api-calling.service';
import { Toastr } from '../../../services/toastr/toastr';
import { environment } from '../../../../environments/environment.development';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faCamera, faClose, faPen } from '@fortawesome/free-solid-svg-icons';
import { AbstractControl, FormBuilder, FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router } from '@angular/router';

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
    private _tostr:Toastr,
    private _fb:FormBuilder,
    private _router:Router
  ){}

  ngOnInit(): void {
    this.loadUser();  // Call this instead of doing logic inline    
  }

  // This function call for get user data.
  loadUser(): void {
  if (this.currentuser) {
      this.getUserDetails(this.currentuser);  // Your existing function
    } else {
      console.warn('User is undefined');
    }
  }

  // Refresh the page after updating any component with the data
  refreshCurrentRoute() {
    // Get current url path
    const currentUrl = this._router.url;

    // Navigate to current user with lication change skip
    this._router.navigateByUrl('/', { skipLocationChange: true }).then(() => {
      this._router.navigate([currentUrl]);
    });
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

  // FUNCTIONS
  // Fetch current user details
  getUserDetails(id:User){
    this._apiCall.getApi("auth/user-details/", { "id":id }).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          this.userDetails = response.data;
          // MAKE FORMS
          // Personal details
          this.updateForm = this._fb.group({
            id: [this.userDetails.id],
            name: [this.userDetails.name, Validators.compose([Validators.required])],
            surname: [this.userDetails.surname, Validators.compose([Validators.required])],
            email: [this.userDetails.email, Validators.compose([Validators.required])],
            school: [this.userDetails.school, Validators.compose([Validators.required])],
            work: [this.userDetails.work, Validators.compose([Validators.required])],
            website: [this.userDetails.website, Validators.compose([Validators.required])],
            city: [this.userDetails.city, Validators.compose([Validators.required])],
            desc: [this.userDetails.description, Validators.compose([Validators.required])]
          }, {validators: this.emailOrNumberAllow});

          // Change password and Username
          this.changePasswordForm = this._fb.group({
            id: [id],
            username: [this.userDetails.username, Validators.compose([Validators.required])],
            password: [this.userDetails.password, Validators.compose([Validators.required, Validators.minLength(8)])]
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
  updateProfile(){
    let updateData:UpdatePersonalDetails = {
      id: this.updateForm.value.id!,
      name: this.updateForm.value.name!,
      surname: this.updateForm.value.surname!,
      email: this.updateForm.value.email!,
      school: this.updateForm.value.school!,
      work: this.updateForm.value.work!,
      website: this.updateForm.value.website!,
      city: this.updateForm.value.city!,
      desc: this.updateForm.value.desc!,
    }

    this._apiCall.putApi("auth/profile/", updateData).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-[var(--btn-success)]", response.msg])
        } else {
          console.log(response.errors);
          
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg])
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
      id: this.changePasswordForm.value.id!,      
      username: this.changePasswordForm.value.username!,
      password: this.changePasswordForm.value.password!,
    }

    this._apiCall.putApi("auth/change-password/", changePassword).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-[var(--btn-success)]", response.msg])
        } else {
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Image uploader function 
  uploader(formData:any){
    this._apiCall.patchApi("auth/profile/", formData).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Update data after response
          this.userDetails = response.data

          // Maybe redirect or show an alert
          this._tostr.toasterStatus(["text-[var(--btn-success)]", response.msg])
        } else {
          console.log(response.errors);
          
          this._tostr.toasterStatus(["text-[var(--btn-danger)]", response.msg])
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Banner images change
  updateBanner(event: Event, id:any){
    // For upload image using formdata() object.
    let formData = new FormData();
    // Get File data.
    const file = (event.target as HTMLInputElement)?.files?.[0];

    // If file come, assign it to formData
    if (file) {
      formData.append('id', id);                        // Add user ID
      formData.append('file', file);                    // Actual File object
      formData.append('imeType', 'banner');             // Other metadata
    }

    // Call image uploader function
    this.uploader(formData)
  }

  // Profile image
  updateUserImage(event: Event, id:any){
    // For upload image using formdata() object.
    let formData = new FormData();
    // Get File data.
    const file = (event.target as HTMLInputElement)?.files?.[0];

    // If file come, assign it to formData
    if (file) {
      formData.append('id', id);                        // Add user ID
      formData.append('file', file);                    // Actual File object
      formData.append('imeType', 'profile');             // Other metadata
    }

    // Call image uploader function
    this.uploader(formData)
  }
}
