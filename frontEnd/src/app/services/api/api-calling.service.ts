import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http'
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment.development';

@Injectable({
  providedIn: 'root'
})
export class ApiCallingService {

  constructor(private _httpClient:HttpClient) { }
  
  // Get api for fetch data.
  getApi(apiRoute:any): Observable<any>{    
    return this._httpClient.get(`${environment.BACKEND_BASEURL}${apiRoute}`, { withCredentials: true });
  }

  // Get api for pagination data fetch.
  getPaginateApi(apiRoute:any): Observable<any>{  
    return this._httpClient.get(`${apiRoute}`, { withCredentials: true });
  }

  // Get api for fetch data for particular id.
  getApiById(apiRoute:any): Observable<any>{
    return this._httpClient.get(`${environment.BACKEND_BASEURL}${apiRoute}`, { withCredentials: true });
  }

  // Post api for save data.
  postApi(apiRoute:any, data:any=null): Observable<any>{
    return this._httpClient.post(`${environment.BACKEND_BASEURL}${apiRoute}`, data, { withCredentials: true });
  }

  // Patch api for half modify data.
  patchApi(apiRoute:any, data:any=null): Observable<any>{
    return this._httpClient.patch(`${environment.BACKEND_BASEURL}${apiRoute}`, data, { withCredentials: true });
  }

  // Put api for update whole modify data.
  putApi(apiRoute:any, data:any=null): Observable<any>{
    return this._httpClient.put(`${environment.BACKEND_BASEURL}${apiRoute}`, data, { withCredentials: true });
  }

  // Delete api for delete particular data.
  deleteApi(apiRoute:any): Observable<any>{
    return this._httpClient.delete(`${environment.BACKEND_BASEURL}${apiRoute}`, { withCredentials: true });
  }
}
