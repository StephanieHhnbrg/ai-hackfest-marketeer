import { Injectable } from '@angular/core';
import {Campaign} from '../data/campaign.data';
import {Observable, Subject} from 'rxjs';
import {environment} from '../../environments/environment';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {SalesEvent} from '../data/event.data';
import {WebpageMetrics} from '../data/metrics.data';

@Injectable({
  providedIn: 'root'
})
export class HttpService {

  private campaignsGenerated$ = new Subject<Campaign[]>();

  constructor(private http: HttpClient) { }

  public getAllCampaigns(): Observable<Campaign[]> {
    let endpoint = environment.getAllCampaignsEndpoint;
    return this.callGCloudRunGetRequest(endpoint);
  }

  public getCampaignsGeneratedAsObservable(): Observable<Campaign[]> {
    return this.campaignsGenerated$.asObservable();
  }

  public getAllEvents(): Observable<SalesEvent[]> {
    let endpoint = environment.getAllEventsEndpoint;
    return this.callGCloudRunGetRequest(endpoint);
  }

  public getWebpageMetrics(): Observable<WebpageMetrics> {
    let endpoint = environment.getWebpageMetricsEndpoint;
    return this.callGCloudRunGetRequest(endpoint);
  }

  public registerEvent(event: SalesEvent) {
    let endpoint = environment.addEventEndpoint;
    return this.callGCloudRunPostRequest(endpoint, event).subscribe({
      next: (response: {campaigns: Campaign[]}) => {
        console.log(response.campaigns);
        event.campaign = event.campaign.concat(response.campaigns.map(c => `${c.name} ${c.variant}`))
        this.campaignsGenerated$.next(response.campaigns);
      },
      error: (err) => console.error('HTTP error:', err)
    });
  }

  private callGCloudRunGetRequest(endpoint: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    };
    return this.http.get<any>(endpoint, httpOptions);
  }

  private callGCloudRunPostRequest(endpoint: string, payload: any): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type':  'application/json',
      })
    };
    return this.http.post<any>(endpoint, JSON.stringify(payload), httpOptions);
  }
}
