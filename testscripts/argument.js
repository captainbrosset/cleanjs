Aria.classDefinition({
	$constructor : function (context, recorders, animationLoop, timer) {
		this.$GameEngine.constructor.apply(this, arguments);
    	this.__colliderResolver = new this.$ColliderResolverImpl();
	},
	$prototype: {
		getResolver: function() {
			return this.__colliderResolver;
		}
	}
});