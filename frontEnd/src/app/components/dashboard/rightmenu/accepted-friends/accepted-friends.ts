import { Component, OnInit } from '@angular/core';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';
import { ApiCallingService } from '../../../../services/api/api-calling.service';
import { UserDataStore } from '../../../../services/userData/user-data-store';

@Component({
  selector: 'app-accepted-friends',
  imports: [FontAwesomeModule],
  templateUrl: './accepted-friends.html',
  styleUrl: './accepted-friends.css'
})
export class AcceptedFriends implements OnInit {
  icon={faChevronRight};
  currentUser:any;
  allFriends:any;

  // Constructor
  constructor(    
    private _apiCall:ApiCallingService,
    private _userData:UserDataStore,
  ){}

  ngOnInit(): void {
    // Get current user id
    this._userData.user$.subscribe(val => { 
      this.currentUser = val?.userId; 
    });

    // Call the all friends
    this.getFriends(this.currentUser)
  }

  // Get all friends
  getFriends(currentUser:any){
    
  }
}
