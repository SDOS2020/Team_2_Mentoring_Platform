var STORAGE_KEY = "todos-vuejs-2.0";
var todoStorage = {
	fetch: function() {
		var todos = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
		todos.forEach(function(todo, index) {
			todo.id = index;
		});
		todoStorage.uid = todos.length;
		return todos;
	},
	save: function(todos) {
		localStorage.setItem(STORAGE_KEY, JSON.stringify(todos));
	}
};

// visibility filters
var filters = {
	all: function(todos) {
		return todos;
	},
	active: function(todos) {
		return todos.filter(function(todo) {
			return !todo.completed;
		});
	},
	completed: function(todos) {
		return todos.filter(function(todo) {
			return todo.completed;
		});
	}
};


const ToDoComponent = {
	delimiters: ["[[", "]]"],

	template:
		`
		<section class="todoapp">
			<header class="header">
				<h1>Todos</h1>
				<input
					class="new-todo"
					autofocus
					autocomplete="off"
					placeholder="What needs to be done?"
					v-model="newTodo"
					@keyup.enter="addTodo"
					style="background-color: #404065 !important; color: #fff !important;"
				/>
			</header>
			<section class="main" v-show="todos.length" v-cloak>
				<input
					id="toggle-all"
					class="toggle-all"
					type="checkbox"
					v-model="allDone"
				/>
				<label for="toggle-all"></label>
				<section  style="height: 35vh; overflow-y: scroll;">	
					<ul class="todo-list">
						<li
							v-for="todo in filteredTodos"
							class="todo"
							:key="todo.id"
							:class="{ completed: todo.completed, editing: todo == editedTodo }"
						>
							<div class="view">
								<input class="toggle" type="checkbox" v-model="todo.completed" />
								<label id="editTodoLabel" @click="editTodo(todo)" title="Edit todo"><b>[[ todo.title ]]</b></label>
								<button class="destroy" @click="removeTodo(todo)">
									<font size="4"><i class="fas fa-trash"></i></font>
								</button>
							</div>
							<input
								class="edit"
								type="text"
								v-model="todo.title"
								v-todo-focus="todo == editedTodo"
								@blur="doneEdit(todo)"
								@keyup.enter="doneEdit(todo)"
								@keyup.esc="cancelEdit(todo)"
							/>
						</li>
					</ul>
				</section>
			</section>
			<footer class="footer" v-show="todos.length" v-cloak>
				<span class="todo-count">
					<strong>[[ remaining ]]</strong> [[ remaining | pluralize ]] left
				</span>
				<button
					class="clear-completed"
					@click="removeCompleted"
					v-show="todos.length > remaining"
				>
					Clear completed
				</button>
			</footer>
		</section>
		`,

	props: {
		username: {required: true},
	},

	data() {
		return {
			todos: todoStorage.fetch(),
			newTodo: "",
			editedTodo: null,
			visibility: "all"
		};
	},

	// watch todos change for localStorage persistence
	watch: {
		todos: {
			handler: function(todos) {
				todoStorage.save(todos);
			},
			deep: true
		}
	},

	// computed properties
	// http://vuejs.org/guide/computed.html
	computed: {
		filteredTodos: function() {
			return filters[this.visibility](this.todos);
		},
		remaining: function() {
			return filters.active(this.todos).length;
		},
		allDone: {
			get: function() {
				return this.remaining === 0;
			},
			set: function(value) {
				this.todos.forEach(function(todo) {
					todo.completed = value;
				});
			}
		}
	},

	filters: {
		pluralize: function(n) {
			return n === 1 ? "item" : "items";
		}
	},

	// methods that implement data logic.
	// note there's no DOM manipulation here at all.
	methods: {
		addTodo: function() {
			var value = this.newTodo && this.newTodo.trim();
			if (!value) {
				return;
			}
			this.todos.push({
				'id': todoStorage.uid++,
				'title': value,
				'completed': false
			});
			this.newTodo = "";
		},

		removeTodo: function(todo) {
			this.todos.splice(this.todos.indexOf(todo), 1);
		},

		editTodo: function(todo) {
			this.beforeEditCache = todo.title;
			this.editedTodo = todo;
		},

		doneEdit: function(todo) {
			if (!this.editedTodo) {
				return;
			}
			this.editedTodo = null;
			todo.title = todo.title.trim();
			if (!todo.title) {
				this.removeTodo(todo);
			}
		},

		cancelEdit: function(todo) {
			this.editedTodo = null;
			todo.title = this.beforeEditCache;
		},

		removeCompleted: function() {
			this.todos = filters.active(this.todos);
		}
	},

	// a custom directive to wait for the DOM to be updated
	// before focusing on the input field.
	// http://vuejs.org/guide/custom-directive.html
	directives: {
		"todo-focus": function(el, binding) {
			if (binding.value) {
				el.focus();
			}
		}
	}
};


// handle routing
function onHashChange() {
	var visibility = window.location.hash.replace(/#\/?/, "");
	if (filters[visibility]) {
		app.visibility = visibility;
	} else {
		window.location.hash = "";
		app.visibility = "all";
	}
}

window.addEventListener("hashchange", onHashChange);
onHashChange();
