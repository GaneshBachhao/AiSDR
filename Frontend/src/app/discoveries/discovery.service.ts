import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  CreateDiscoveryRequestDTO,
  DiscoveryResponseDTO,
  UpdateDiscoveryRequestDTO,
} from './discovery.models';

@Injectable({ providedIn: 'root' })
export class DiscoveryService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/discoveries`;

  list(): Observable<DiscoveryResponseDTO[]> {
    return this.http.get<DiscoveryResponseDTO[]>(this.base, {
      params: new HttpParams().set('limit', 500),
    });
  }

  search(searchText: string): Observable<DiscoveryResponseDTO[]> {
    return this.http.get<DiscoveryResponseDTO[]>(`${this.base}/search`, {
      params: new HttpParams().set('search_text', searchText).set('limit', 500),
    });
  }

  get(id: string): Observable<DiscoveryResponseDTO> {
    return this.http.get<DiscoveryResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateDiscoveryRequestDTO): Observable<DiscoveryResponseDTO> {
    return this.http.post<DiscoveryResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateDiscoveryRequestDTO): Observable<DiscoveryResponseDTO> {
    return this.http.put<DiscoveryResponseDTO>(`${this.base}/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
