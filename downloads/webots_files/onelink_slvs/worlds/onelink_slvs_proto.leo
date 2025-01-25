<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: https://leo-editor.github.io/leo-editor/leo_toc.html -->
<leo_file xmlns:leo="https://leo-editor.github.io/leo-editor/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="leo.20250125233710.2"><vh>original onlink_proto</vh></v>
<v t="leo.20250125233733.1"><vh>@clean onelink_leo1.wbt</vh>
<v t="leo.20250126000845.1"><vh>#VRML</vh></v>
<v t="leo.20250126051919.1"><vh>EXTERNPROTO</vh></v>
<v t="leo.20250126001100.1"><vh>WorldInfo</vh></v>
<v t="leo.20250126052014.1"><vh>Viewpoint</vh>
<v t="leo.20250126053237.1"><vh>orientation</vh></v>
<v t="leo.20250126053300.1"><vh>position</vh></v>
</v>
<v t="leo.20250126052035.1"><vh>TextureBackground</vh></v>
<v t="leo.20250126052058.1"><vh>TextureBackgroundLight</vh></v>
<v t="leo.20250126052115.1"><vh>RectangleArena</vh></v>
<v t="leo.20250126001114.1"><vh>Robot</vh>
<v t="leo.20250126001233.1"><vh>children</vh>
<v t="leo.20250126052149.1"><vh>Solid</vh>
<v t="leo.20250126052212.1"><vh>children</vh>
<v t="leo.20250126052234.1"><vh>BaseSolid</vh></v>
<v t="leo.20250126052300.1"><vh>HingeJoint</vh>
<v t="leo.20250126052331.1"><vh>jointParameters</vh>
<v t="leo.20250126053351.1"><vh>axis</vh></v>
</v>
<v t="leo.20250126052408.1"><vh>device</vh>
<v t="leo.20250126052511.1"><vh>RotationalMotor</vh>
<v t="leo.20250126053117.1"><vh>name</vh></v>
</v>
</v>
<v t="leo.20250126052433.1"><vh>endPoint</vh>
<v t="leo.20250126052552.1"><vh>children</vh>
<v t="leo.20250126052615.1"><vh>JointSolid</vh></v>
<v t="leo.20250126052634.1"><vh>Solid</vh>
<v t="leo.20250126052730.1"><vh>children</vh>
<v t="leo.20250126052754.1"><vh>LinkSolid</vh></v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
</v>
<v t="leo.20250126001238.1"><vh>controller</vh></v>
</v>
</v>
<v t="leo.20250125235802.1"><vh>@path ./../controllers/joint_controller</vh>
<v t="leo.20250125235721.1"><vh>@auto joint_controller.py</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="leo.20250125233710.2">#VRML_SIM R2023b utf8

EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"

WorldInfo {}
Viewpoint {
  orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868
  position 0.7495096875887461 -3.1141998018989674 1.7796380905257032
}
TexturedBackground {}
TexturedBackgroundLight {}
RectangleArena {}

Robot {
  children [
    Solid {
      children [
        BaseSolid { }  # Instantiate the BaseSolid PROTO
        HingeJoint {
          jointParameters HingeJointParameters {
            axis 0 0 1
          }
          device [
            RotationalMotor {
              name "joint_motor"
            }
          ]
          endPoint Solid {
            children [
              JointSolid { }  # Instantiate the JointSolid PROTO
              Solid {
                children [
                  LinkSolid { }  # Instantiate the LinkSolid PROTO
                ]
              }
            ]
          }
        }
      ]
    }
  ]
  controller "joint_controller"
}</t>
<t tx="leo.20250125233733.1">@others
</t>
<t tx="leo.20250125235802.1"></t>
<t tx="leo.20250126000845.1">#VRML_SIM R2023b utf8
</t>
<t tx="leo.20250126001100.1">WorldInfo {}
</t>
<t tx="leo.20250126001114.1">Robot {
    @others
}
</t>
<t tx="leo.20250126001233.1">children [
    @others
]
</t>
<t tx="leo.20250126001238.1">controller "joint_controller"</t>
<t tx="leo.20250126051919.1">EXTERNPROTO "../protos/TexturedBackground.proto"
EXTERNPROTO "../protos/TexturedBackgroundLight.proto"
EXTERNPROTO "../protos/RectangleArena.proto"
EXTERNPROTO "../protos/BaseSolid.proto"
EXTERNPROTO "../protos/JointSolid.proto"
EXTERNPROTO "../protos/LinkSolid.proto"</t>
<t tx="leo.20250126052014.1">Viewpoint {
    @others
}
</t>
<t tx="leo.20250126052035.1">TexturedBackground {}
</t>
<t tx="leo.20250126052058.1">TexturedBackgroundLight {}
</t>
<t tx="leo.20250126052115.1">RectangleArena {}
</t>
<t tx="leo.20250126052149.1">Solid {
    @others
}</t>
<t tx="leo.20250126052212.1">children [
    @others
]</t>
<t tx="leo.20250126052234.1">BaseSolid { }  # Instantiate the BaseSolid PROTO
</t>
<t tx="leo.20250126052300.1">HingeJoint {
    @others
}</t>
<t tx="leo.20250126052331.1">jointParameters HingeJointParameters {
    @others
}


</t>
<t tx="leo.20250126052408.1">device [
    @others
]</t>
<t tx="leo.20250126052433.1">endPoint Solid {
    @others
}</t>
<t tx="leo.20250126052511.1">RotationalMotor {
    @others
}</t>
<t tx="leo.20250126052552.1">children [
    @others
]</t>
<t tx="leo.20250126052615.1">JointSolid { }  # Instantiate the JointSolid PROTO
</t>
<t tx="leo.20250126052634.1">Solid {
    @others
}</t>
<t tx="leo.20250126052730.1">children [
    @others
]</t>
<t tx="leo.20250126052754.1">LinkSolid { }  # Instantiate the LinkSolid PROTO</t>
<t tx="leo.20250126053117.1">name "joint_motor"</t>
<t tx="leo.20250126053237.1">orientation -0.17911760145636924 0.20303955404969007 0.9626483388755317 1.7931226479511868</t>
<t tx="leo.20250126053300.1">position 0.7495096875887461 -3.1141998018989674 1.7796380905257032</t>
<t tx="leo.20250126053351.1">axis 0 0 1</t>
</tnodes>
</leo_file>
