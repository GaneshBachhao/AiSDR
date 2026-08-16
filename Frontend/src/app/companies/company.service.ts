import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import { CompanyResponseDTO, CreateCompanyRequestDTO, UpdateCompanyRequestDTO } from './company.models';

@Injectable({ providedIn: 'root' })
export class CompanyService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/companies`;

  list(): Observable<CompanyResponseDTO[]> {
    return this.http.get<CompanyResponseDTO[]>(this.base, {
      params: new HttpParams().set('limit', 500),
    });
  }

  search(query: string): Observable<CompanyResponseDTO[]> {
    return this.http.get<CompanyResponseDTO[]>(`${this.base}/search`, {
      params: new HttpParams().set('query', query).set('limit', 500),
    });
  }

  get(id: string): Observable<CompanyResponseDTO> {
    return this.http.get<CompanyResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateCompanyRequestDTO): Observable<CompanyResponseDTO> {
    return this.http.post<CompanyResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateCompanyRequestDTO): Observable<CompanyResponseDTO> {
    return this.http.put<CompanyResponseDTO>(`${this.base}/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
