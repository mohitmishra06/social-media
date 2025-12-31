import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserDataStore {
  // Store user object
  // glbUserData:BehaviorSubject<any>=new BehaviorSubject<any>({})
  private userSource = new BehaviorSubject<any>(null);
  user$ = this.userSource.asObservable();

  setUser(user: any) {
    this.userSource.next(user);
  }

  getUser() {
    return this.userSource.value;
  }

}
