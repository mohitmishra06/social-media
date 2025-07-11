import { Component, OnInit } from '@angular/core';
import { Toastr } from '../../services/toastr/toastr';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-toastr',
  imports: [CommonModule],
  templateUrl: './toastr.html',
  styleUrl: './toastr.css'
})
export class ToasterComponent implements OnInit{
  toasterValue: any;
  constructor(private _toaster:Toastr){}

  ngOnInit(): void {
    this._toaster.toasterValue.subscribe((res)=>{
      this.toasterValue = res;      
      // When toasterValue have value.
      if(this.toasterValue !== ''){
        this.closeToastr();
      }
    });
  }

  // Toaster close automatically.
  closeToastr(){
    // window.setTimeout(()=>{
    //   this.toasterValue = '';      
    // }, 5000);

    setTimeout(()=>{
      this.toasterValue = '';
    }, 4000);
  }
}
