const ShowToDo = {
	delimiters: ["[[", "]]"],
	template: `
	<div>
		<div class="card-header" style="border-radius: 10px 10px 0 0; background-color: lightgrey;">
			<center>
				<font size="4">
					<b>To-Do List</b>
				</font>
			</center>
		</div>

		<div style="height: 30vh; overflow-y: scroll;">
			<div v-if="todos.length === 0" id="no-todos-text">
				<center style="margin-top: 5rem;">
					<b>Woohoo!</b> No work due soon!
				</center>
			</div>

			<table class="table table-hover table-striped">
				<tbody>
					<tr v-for="todo in todos">
						<td colspan="2">
							<b>[[ todo.task ]]</b>
							<br/>
							<i>
								<small class="text-muted">
									Due <b> [[ todo.deadline_time ]] </b> [[ todo.deadline_date ]], [[ todo.deadline_day ]]
								</small>
							</i>
						</td>
						<td>
							<input type="checkbox"></input> 
						</td>
					</tr>
				</tbody>
			</table>
		</div>
	</div>
	`,
	data() {
		return {
			todos: [],
		};
	},

	props: {
		username: {
			required: true
		}
	},

	created() {
		this.get_todos();
		window.setInterval(this.get_todos, 1000);
	},

	methods: {
		get_todos() {
			let request_url = "http://127.0.0.1:8000/api/get_todos/" + this.guest_name;

			axios.get(request_url)
			.then(response => {
				this.todos = response.data.todos;
			})
			.catch(error => {
				console.log('[ERROR]');
				console.log(error);
			});
		}
	}
};
