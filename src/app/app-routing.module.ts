import { HomeComponent } from './components/home/home.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { AddmodComponent } from './components/addmod/addmod.component';

const routes: Routes = [
    {
        path: '',
        component: HomeComponent
    },
    {
        path: 'addmod',
        component: AddmodComponent
    },
    {
        path: 'options',
        component: HomeComponent
    },
];

@NgModule({
    imports: [RouterModule.forRoot(routes, {useHash: true})],
    exports: [RouterModule]
})
export class AppRoutingModule { }
