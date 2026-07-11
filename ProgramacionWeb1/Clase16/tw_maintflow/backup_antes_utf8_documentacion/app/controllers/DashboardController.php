<?php
class DashboardController extends Controller {public function index():void{Auth::requireLogin();$this->view('dashboard/index',['title'=>'Dashboard','m'=>(new Dashboard())->metrics()]);}}

