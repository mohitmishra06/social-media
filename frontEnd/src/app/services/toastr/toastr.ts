import { EventEmitter, Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class Toastr {
  // Toaster data.
  toasterValue = new EventEmitter<any>();
  
  constructor() { }

  /** show toast */
  // show(message?: string){}

  /** show successful toast */
  toasterStatus(toasterData?: string[]){
    this.toasterValue.emit(toasterData);    
  }
}
