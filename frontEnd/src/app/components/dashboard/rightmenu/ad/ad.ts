import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-ad',
  imports: [],
  templateUrl: './ad.html',
  styleUrl: './ad.css'
})
export class Ad implements OnInit{
  @Input() size?:string;
  
  ngOnInit(): void {    
  }
}
