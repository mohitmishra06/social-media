import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserDataStore {
  // Store user object
  glbUserData:BehaviorSubject<any>=new BehaviorSubject<any>({})
  constructor() { }

  // Function store the coming user data
  setUserData(userData?:any){
    this.glbUserData.next(userData)
  }

}
