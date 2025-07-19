import { Component, OnInit } from '@angular/core';
import { faRightFromBracket, faUser, faUsers } from '@fortawesome/free-solid-svg-icons';
import { MobileMenuComponent } from '../mobile-menu/mobile-menu';
import { CommonModule } from '@angular/common';
import { Toastr } from '../../services/toastr/toastr';
import { ApiCallingService } from '../../services/api/api-calling.service';
import { Router } from '@angular/router';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { UserDataStore } from '../../services/userData/user-data-store';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule, MobileMenuComponent, FontAwesomeModule],
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.css']
})
export default class NavbarComponent implements OnInit {
  icon = { faRightFromBracket, faUser }
  userImg:string = '';

  constructor(
    private _apiCall:ApiCallingService,
    private _router:Router,
    private _tostr:Toastr,
    private _userData:UserDataStore
  ){}

  ngOnInit(): void {
    this._userData.glbUserData.subscribe(val=>{
      this.userImg = val.userImg
    })
  }

  // Logout the session
  logout(){
    // Call api for authorisation.
    this._apiCall.putApi('auth/logout/').subscribe({
      // next() method will be executed only when there will be no error.
      next :(response:any) => {
        // On success.
        if(response.status === false){
            this._tostr.toasterStatus(['text-gray-500', response.msg]);
            return;
          }
          this._tostr.toasterStatus(['text-gray-600', response.msg]);
          this._router.navigate(['/auth']);
          return;
      }
    });
  }
}
