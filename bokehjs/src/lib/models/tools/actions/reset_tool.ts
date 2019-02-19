import {ActionTool, ActionToolView} from "./action_tool"
import * as p from "core/properties"

export class ResetToolView extends ActionToolView {
  model: ResetTool

  doit(): void {
    this.plot_view.reset()
  }
}

export namespace ResetTool {
  export type Attrs = p.AttrsOf<Props>

  export type Props = ActionTool.Props
}

export interface ResetTool extends ResetTool.Attrs {}

export class ResetTool extends ActionTool {
  properties: ResetTool.Props

  constructor(attrs?: Partial<ResetTool.Attrs>) {
    super(attrs)
  }

  static initClass(): void {
    this.prototype.type = "ResetTool"
    this.prototype.default_view = ResetToolView
  }

  tool_name = "Reset"
  icon = "bk-tool-icon-reset"
}
ResetTool.initClass()
