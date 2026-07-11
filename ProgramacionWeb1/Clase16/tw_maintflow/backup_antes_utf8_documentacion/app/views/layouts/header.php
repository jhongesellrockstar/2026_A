<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title><?=htmlspecialchars($title??APP_NAME)?> | <?=APP_NAME?></title><link rel="stylesheet" href="<?=BASE_URL?>/assets/css/estilos.css"></head><body>
<header class="top"><a class="brand" href="<?=BASE_URL?>/">TW <b>MaintFlow</b></a><button class="menu" aria-label="Menú">☰</button><?php if(Auth::check()):?><span><?=htmlspecialchars(Auth::user()['nombre'])?> · <?=htmlspecialchars(Auth::user()['rol'])?></span><?php endif;?></header>
<?php if(Auth::check()) require APP_ROOT.'/app/views/layouts/sidebar.php';?><main class="<?=Auth::check()?'content':''?>"><?php if($msg=Session::flash('ok')):?><div class="alert ok"><?=htmlspecialchars($msg)?></div><?php endif;?>

