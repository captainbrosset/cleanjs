Aria.classDefinition({
	$classpath : 'samples.games.nyump.collision.BulletEnemyCollider',
	$extends : 'samples.games.common.BaseObject',
	$dependencies : [],
	$implements : ['samples.games.common.collision.Collider'],
	$constructor : function () {
		this.$BaseObject.constructor.call(this);
		this.test = 2;
	},
	$prototype : {
		collide : function (bullet, enemy) {
			bullet.destroy();
			enemy.destroy();
		}
	}
});