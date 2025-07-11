import { Component, OnInit } from '@angular/core';
import NavbarComponent from '../navbar/navbar';
import { RouterOutlet } from '@angular/router';
import { ApiCallingService } from '../../services/api/api-calling.service';
import { UserDataStore } from '../../services/userData/user-data-store';

@Component({
  selector: 'app-layout',
  standalone:true,
  imports: [NavbarComponent, RouterOutlet],
  templateUrl: './layout.html',
  styleUrls: ['./layout.css']
})
export class LayoutComponent implements OnInit {
  constructor(private _apiCall:ApiCallingService, private _userData:UserDataStore){}

  ngOnInit(): void {
    // Call api for authorisation.
    this._apiCall.getApi('auth/user-session-data/').subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {        
        // On success.
        if(response.status === true){
            console.log(response);
            
            this._userData.setUserData(response.data)
            return;
          }
          return;
        }
    });
  }
}
