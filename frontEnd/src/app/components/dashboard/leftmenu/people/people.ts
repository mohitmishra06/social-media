import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faChevronRight, faClose, faPeopleGroup } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { UserDataStore } from '../../../../services/userData/user-data-store';
import { RouterModule } from '@angular/router';
import { environment } from '../../../../../environments/environment.development';

@Component({
  selector: 'app-people',
  imports: [CommonModule, FontAwesomeModule, RouterModule],
  templateUrl: './people.html',
  styleUrl: './people.css'
})
export class People implements OnInit {
  @Input() location?:string;  // Parents props
  icon = { faPeopleGroup, faChevronRight, faClose};
  isOpenModal:boolean = false;    // IsOpenModal toggale
  peoples:any;
  url:string="";
  currentUser:any;
  loggedUser:any;

  // Constructor
  constructor(
    private _apiCall:ApiCallingService,
    private _userData:UserDataStore
  ){}
  
  ngOnInit(){
    // Get current user id
    this._userData.user$.subscribe(val => { 
      this.currentUser = val?.userId; 
      this.loggedUser = val?.user; 
    });

    // Img url
    this.url = environment.IMG_BASEURL;

    // Get all users
    this.allUsers()
  }

  // Open Modal
  toggleModal(){
    this.isOpenModal = (this.isOpenModal === true) ? false : true;  // If modal is open then set false or true
  }

  // Get all users
  allUsers(){
    // Call api for saving data
    this._apiCall.getApi("auth/all-users", {}).subscribe({
      next: (response: any) => {
        if (response.status === true) {
          // Get all stories
          this.peoples = response.data;          
        }
      },
      error: (err) => {
        console.error("API call failed", err);
      }
    });
  }

  // Request send
  sendRequest(followingID:any, followerID:any){
    console.log(followingID);
    console.log(followerID);    
  }
}
