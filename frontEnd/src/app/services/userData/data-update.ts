import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DataUpdate {
  private refreshSource = new Subject<void>();
  data$ = this.refreshSource.asObservable();

  notifyForNewData() {
    this.refreshSource.next();
  }
}
