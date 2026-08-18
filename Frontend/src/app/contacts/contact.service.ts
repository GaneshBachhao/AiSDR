import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';
import {
  ContactResponseDTO,
  CreateContactRequestDTO,
  UpdateContactRequestDTO,
} from './contact.models';

/** Note: unlike /companies/search (`query`), /contacts/search uses
 * `search_text` -- verified against the generated schema, not assumed
 * from the Company module's convention. Per-router param names are not
 * uniform in this backend; check each one, don't copy-paste. */
@Injectable({ providedIn: 'root' })
export class ContactService {
  private readonly http = inject(HttpClient);
  private readonly base = `${environment.apiBaseUrl}/contacts`;

  list(): Observable<ContactResponseDTO[]> {
    return this.http.get<ContactResponseDTO[]>(this.base, {
      params: new HttpParams().set('limit', 500),
    });
  }

  search(searchText: string): Observable<ContactResponseDTO[]> {
    return this.http.get<ContactResponseDTO[]>(`${this.base}/search`, {
      params: new HttpParams().set('search_text', searchText).set('limit', 500),
    });
  }

  get(id: string): Observable<ContactResponseDTO> {
    return this.http.get<ContactResponseDTO>(`${this.base}/${id}`);
  }

  create(dto: CreateContactRequestDTO): Observable<ContactResponseDTO> {
    return this.http.post<ContactResponseDTO>(this.base, dto);
  }

  update(id: string, dto: UpdateContactRequestDTO): Observable<ContactResponseDTO> {
    return this.http.put<ContactResponseDTO>(`${this.base}/${id}`, dto);
  }

  remove(id: string): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
